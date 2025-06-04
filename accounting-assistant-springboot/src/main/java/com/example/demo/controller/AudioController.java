package com.example.demo.controller;

import com.example.demo.config.AppConstants;
import com.example.demo.tabs.*;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.sound.sampled.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.*;

@RestController
@RequestMapping("/api/audio")
public class AudioController {

    private boolean recording = false;
    private final int RATE = 44100;
    private final int DURATION = 10;

    @GetMapping("/recording")
    public ResponseEntity<?> controlRecording(@RequestParam String action) {
        if (action.equals("start") && !recording) {
            recording = true;
            Executors.newSingleThreadExecutor().submit(this::startRecording);
            return ResponseEntity.ok(Map.of("status", "Recording started"));
        } else if (action.equals("stop") && recording) {
            recording = false;
            return ResponseEntity.ok(Map.of("status", "Recording stopped, processing audio..."));
        }
        return ResponseEntity.badRequest().body(Map.of("status", "Invalid request"));
    }

    private void startRecording() {
        File outputFile = new File(AppConstants.TRANSCRIBE_OUTPUT_PATH.getParent().toFile(), "temp_recording.wav");
        AudioFormat format = new AudioFormat(RATE, 16, 1, true, false);

        try {
            System.out.println("Starting recording...");
            DataLine.Info info = new DataLine.Info(TargetDataLine.class, format);
            TargetDataLine microphone = (TargetDataLine) AudioSystem.getLine(info);
            microphone.open(format);
            microphone.start();

            byte[] buffer = new byte[4096];
            try (ByteArrayOutputStream out = new ByteArrayOutputStream()) {
                long end = System.currentTimeMillis() + (DURATION * 1000L);
                while (System.currentTimeMillis() < end && recording) {
                    int bytesRead = microphone.read(buffer, 0, buffer.length);
                    out.write(buffer, 0, bytesRead);
                }

                byte[] audioData = out.toByteArray();
                Files.write(outputFile.toPath(), audioData);
                System.out.println("Audio recording saved to: " + outputFile.getAbsolutePath());
                handleRecording(outputFile);
            }

            microphone.stop();
            microphone.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void handleRecording(File audioFile) {
        try {
            String transcript = transcribeAudio(audioFile);
            System.out.println("Transcript: " + transcript);
            callAppropriateTab(transcript);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private String transcribeAudio(File audioFile) throws IOException, InterruptedException {
        File convertedWav = new File(AppConstants.TRANSCRIBE_OUTPUT_PATH.getParent().toFile(), "output.wav");

        List<String> ffmpegCmd = List.of(
                AppConstants.FFMPEG_EXECUTABLE, "-i", audioFile.getAbsolutePath(),
                "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
                convertedWav.getAbsolutePath()
        );
        Process ffmpegProcess = new ProcessBuilder(ffmpegCmd).redirectErrorStream(true).start();
        ffmpegProcess.waitFor();

        List<String> whisperCmd = List.of(
                AppConstants.WHISPER_CPP_EXECUTABLE, "-f", convertedWav.getAbsolutePath(),
                "--model", AppConstants.MODEL_PATH.toString(), "-otxt", AppConstants.TRANSCRIBE_OUTPUT_PATH.toString(),
                "--language", "en"
        );
        Process whisperProcess = new ProcessBuilder(whisperCmd).redirectErrorStream(true).start();
        whisperProcess.waitFor();

        File outputText = AppConstants.TRANSCRIBE_OUTPUT_PATH.toFile();
        String transcript = Files.readString(outputText.toPath());

//        Files.walk(AppConstants.TRANSCRIBE_OUTPUT_PATH.getParent())
//                .map(Path::toFile)
//                .filter(f -> !f.isDirectory())
//                .forEach(File::delete);

        return transcript;
    }

    private void callAppropriateTab(String transcript) throws IOException, InterruptedException {
        // This assumes your tab_classifier.py accepts model_path and transcript as arguments
        String classifierScript = "src/main/resources/scripts/tab_classifier.py";

        Process process = new ProcessBuilder(
                "python3",
                classifierScript,
                AppConstants.TAB_MODEL_PATH.toAbsolutePath().toString(),
                transcript
        ).redirectErrorStream(true).start();

        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        String tabClass = reader.readLine();
        process.waitFor();

        switch (tabClass) {
            case "Product" -> new ProductLogic().appropriateFunction(transcript);
            case "Client" -> new ClientLogic().appropriateFunction(transcript);
            case "Invoice" -> new InvoiceLogic().appropriateFunction(transcript);
            case "Vendor" -> new VendorLogic().appropriateFunction(transcript);
            default -> System.out.println("No matching class found for tab: " + tabClass);
        }
    }
}
