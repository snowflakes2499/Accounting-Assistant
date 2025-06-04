package com.example.demo.config;

import java.nio.file.Path;
import java.nio.file.Paths;

public class AppConstants {

    // Executables
    public static final String WHISPER_CPP_EXECUTABLE = "/home/suyash/whisper.cpp/build/bin/whisper-cli";
    public static final String FFMPEG_EXECUTABLE = "ffmpeg";

    // Whisper model (absolute)
    public static final Path MODEL_PATH = Paths.get(
        "/home/suyash/whisper.cpp/ggml-base.en.bin"
    );

    // Transcription output (inside project)
    public static final Path TRANSCRIBE_OUTPUT_PATH = Paths.get("media/output.txt");

    // ML model (absolute)
    public static final Path TAB_MODEL_PATH = Paths.get(
        "src/main/resources/models/fast_invoice_ninja_tab_classifier.pkl"
    );

    // Prompt templates (inside project)
    public static final Path PRODUCT_TEMPLATE_PATH = Paths.get("src/main/resources/templates/Product.txt");
    public static final Path CLIENT_TEMPLATE_PATH = Paths.get("src/main/resources/templates/Client.txt");
    public static final Path INVOICE_TEMPLATE_PATH = Paths.get("src/main/resources/templates/Invoice.txt");
    public static final Path VENDOR_TEMPLATE_PATH = Paths.get("src/main/resources/templates/Vendor.txt");
}
