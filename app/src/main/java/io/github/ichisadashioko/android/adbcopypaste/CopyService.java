package io.github.ichisadashioko.android.adbcopypaste;

import android.app.IntentService;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.nio.charset.StandardCharsets;

public class CopyService extends IntentService {
    public static final String OK_INDICATOR_FILEPATH = "/sdcard/io.github.ichisadashioko.android.adbcopypaste/ok";
    public static final String ERROR_INDICATOR_FILEPATH = "/sdcard/io.github.ichisadashioko.android.adbcopypaste/error";
    public static final String DATA_TO_BE_COPIED_FILEPATH = "/sdcard/io.github.ichisadashioko.android.adbcopypaste/data_to_be_copied";
    public static final long MAX_TEXT_FILE_SIZE = 5242880; // 5 MBs

    public CopyService() {
        super(CopyService.class.getName());
    }

    @Override
    protected void onHandleIntent(Intent intent) {
        System.out.println("Hello from CopyService");

        try {
            String text_data_filepath =DATA_TO_BE_COPIED_FILEPATH;
            File text_data_file = new File(text_data_filepath);
            if (!text_data_file.exists()) {
                throw new Exception(text_data_filepath + " does not exist");
            } else {
                if (!text_data_file.isFile()) {
                    throw new Exception(text_data_filepath + " is not a normal file");
                } else {
                    long text_data_file_size_long = text_data_file.length();
                    if (text_data_file_size_long < 1) {
                        throw new Exception(text_data_filepath + " is empty");
                    } else if (text_data_file_size_long > MAX_TEXT_FILE_SIZE) {
                        throw new Exception(text_data_file_size_long + " is unreasonably large");
                    } else {
                        int text_data_file_size = (int) text_data_file_size_long;
                        byte[] text_file_bytes = new byte[text_data_file_size];
                        FileInputStream file_input_stream = new FileInputStream(text_data_file);
                        file_input_stream.read(text_file_bytes);
                        file_input_stream.close();

                        String text_content = new String(text_file_bytes, StandardCharsets.UTF_8);
                        System.out.println(text_content);

                        ClipboardManager clipboard_manager = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
                        ClipData clip_data = ClipData.newPlainText("CopyService", text_content);
                        clipboard_manager.setPrimaryClip(clip_data);

                        File ok_status_file = new File(OK_INDICATOR_FILEPATH);
                        if (!ok_status_file.exists()){
                            if(!ok_status_file.createNewFile()){
                                throw new Exception("cannot create " + ok_status_file.getAbsolutePath());
                            }
                        }
                    }
                }
            }
        } catch (Exception ex) {
            ex.printStackTrace(System.err);

            try{
                File error_status_file = new File(ERROR_INDICATOR_FILEPATH);

                if(!error_status_file.exists()){
                    String parent_filepath = error_status_file.getParent();
                    File parent_file = new File(parent_filepath);
                    if(!parent_file.exists()){
                        if(!parent_file.mkdirs()){
                            throw new Exception("cannot mkdirs " + parent_filepath);
                        }
                    }

                    if(!error_status_file.createNewFile()){
                        throw new Exception("cannot create file " + ERROR_INDICATOR_FILEPATH);
                    }
                }

                String error_message = ex.getMessage();
                FileOutputStream file_output_stream = new FileOutputStream(ERROR_INDICATOR_FILEPATH, false);
                file_output_stream.write(StandardCharsets.UTF_8.encode(error_message).array());
                file_output_stream.close();
                // TODO log stack trace
                // String stack_trace_str = ex.getStackTrace()
            }catch (Exception ex2){
                ex2.printStackTrace(System.err);
            }
        }
    }
}
