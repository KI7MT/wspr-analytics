package com.ki7mt.spark.utils;

import org.apache.commons.io.FileUtils;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.URL;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

public class DownloadArchive {
    public static void main(String[] args) {

        // Check args and exit if not equal to to
        int count = args.length;
        if (count != 2 ) {
            System.err.println("CsvDownload requires (2) arguments, year and month");
            System.err.println("Example: java -jar CsvDownload_2.12.0-1.jar 2008 03");
            System.exit(1);
        }

        // Change the year and two digit month to download
        String year = args[0];
        String month = args[1];


        /* -- NO FURTHER EDITS NEEDED BELOW THIS LINE -- */

        // Process variables
        String fileName;
        fileName = "wsprspots-" + year + "-" + month + ".csv.zip";
        String inFileUrl = "http://wsprnet.org/archive/" + fileName;
        String outFile = "data/csv/" + fileName;
        String outFileDir = "data/csv";

        // Download the file
        System.out.println("* Downloading WSPR Archive File : " + fileName);
        DownloadFile(inFileUrl, outFile);

        // Unzip the file
        UnzipFile(outFile, outFileDir);
        System.out.println("* Finished");

    } // END - main method

    private static void DownloadFile(String inFileUrl, String outFile) {
        try {
            URL url = new URL(inFileUrl);
            File dest_file = new File(outFile);
            FileUtils.copyURLToFile(url, dest_file);
        } catch (IOException e) {
            e.printStackTrace();
            System.exit(2);
        }
    } // END - DownloadFile method

    private static void UnzipFile(String zipFilePath, String destDir) {
        File dir = new File(destDir);
        if (!dir.exists()) {
            dir.mkdirs();
        }
        FileInputStream fis;
        byte[] buffer = new byte[1024];
        try {
            fis = new FileInputStream(zipFilePath);
            ZipInputStream zis = new ZipInputStream(fis);
            ZipEntry ze = zis.getNextEntry();
            while (ze != null) {
                String fileName = ze.getName();
                File newFile = new File(destDir + File.separator + fileName);
                System.out.println("* Unzipping to " + newFile.getAbsolutePath());

                new File(newFile.getParent()).mkdirs();
                FileOutputStream fos = new FileOutputStream(newFile);
                int len;

                while ((len = zis.read(buffer)) > 0) {
                    fos.write(buffer, 0, len);
                }
                fos.close();

                //close this ZipEntry
                zis.closeEntry();
                ze = zis.getNextEntry();
            }
            //close last ZipEntry
            zis.closeEntry();
            zis.close();
            fis.close();
        } catch (IOException e) {
            e.printStackTrace();
            System.exit(2);
        }
    } // END - UnzipFile method

} // END - DownloadFromWsprnet