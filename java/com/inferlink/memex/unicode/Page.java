package com.inferlink.memex.unicode;

import org.json.JSONException;
import org.json.JSONObject;

public class Page {
  
  public static String HASBODYPART = "hasBodyPart";
  public static String HASTITLEPART = "hasTitlePart";
  public static String TEXT = "text";

  public static String UNICODEHISTOGRAM = "unicodeHistogram";
  public static String UNICODETEXT = "unicodeText";
  
  private JSONObject object;
  private UnicodeHistogram bodyHistogram;
  private UnicodeHistogram titleHistogram;

  public Page(String json) {
    try {
      object = new JSONObject(json);
      titleHistogram = processHistogram(HASTITLEPART);
      bodyHistogram = processHistogram(HASBODYPART);
    } catch (JSONException e) {
      e.printStackTrace();
    }
  }

  private UnicodeHistogram processHistogram(String section) throws JSONException {
    JSONObject text = this.object.getJSONObject(section);
    String content = text.getString(TEXT);
    return new UnicodeHistogram(content);
  }
  
  public String getRawUnicodes() {
    return this.titleHistogram.getNonAscii()+this.bodyHistogram.getNonAscii();
  }
  
  public String toJson() throws JSONException {
    if(!bodyHistogram.isEmpty()) {
      JSONObject hasBodyPart = this.object.getJSONObject(HASBODYPART);
      object.remove(HASBODYPART);
      hasBodyPart.put(UNICODEHISTOGRAM, bodyHistogram.toJsonArray());
      hasBodyPart.put(UNICODETEXT, bodyHistogram.getNonAscii());
      object.put(HASBODYPART, hasBodyPart);
    }
    if(!titleHistogram.isEmpty()) {
      JSONObject hasTitlePart = this.object.getJSONObject(HASTITLEPART);
      object.remove(HASTITLEPART);
      hasTitlePart.put(UNICODEHISTOGRAM, titleHistogram.toJsonArray());
      hasTitlePart.put(UNICODETEXT, titleHistogram.getNonAscii());
      object.put(HASTITLEPART, hasTitlePart);
    }
    
    return object.toString();
  }
}
