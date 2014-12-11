package com.inferlink.memex.unicode;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

import org.json.JSONException;

public class Extractor {
  public static void main(String[] args) {
    try(BufferedReader br = new BufferedReader(new InputStreamReader(System.in,"UTF-8"));
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out))) {
      String line = br.readLine();
      String lineParts[] = line.split("\\t");
      
      if(lineParts.length == 2) {
        String ad_uri = lineParts[0];
        String ad_json = lineParts[1];
        
        Page page = new Page(ad_json);
        
        String objectJson = page.toJson();
        bw.write(ad_uri + "\t" + objectJson);
      }
    } catch (IOException e) {
      e.printStackTrace();
    } catch (JSONException e) {
      e.printStackTrace();
    }
  }
}
