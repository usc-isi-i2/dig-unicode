package com.inferlink.memex.unicode;

import org.apache.commons.collections.Bag;
import org.apache.commons.collections.bag.HashBag;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class UnicodeHistogram {
  private String content;
  private String nonascii;
  private String nonAsciiTokens;
  private Bag wordbag = new HashBag();
  
  public UnicodeHistogram(String content) {
    this.content = content;
    nonascii = this.content.replaceAll("[\\p{ASCII}]", "");
    nonAsciiTokens = "";

    //I think there is something up with 65039 ... it should be added with the high surrogate
    //from http://dafoster.net/articles/2013/06/01/handling-text-correctly/
    for (int i=0, n=nonascii.length(); i<n; i++) {
      char c1 = nonascii.charAt(i);
      String character = "";
      character += c1;

      // CORRECT. Handles all Unicode characters.
      int codepoint;
      if (Character.isHighSurrogate(c1)) {
        if (i+1 < n) {
          char c2 = nonascii.charAt(i+1);
          if (Character.isLowSurrogate(c2)) {
            // Surrogate pair
            codepoint = Character.toCodePoint(c1, c2);
            character += c2;
            i++;
          } else {
            // High-surrogate alone
            codepoint = (int) c1;
          }
        } else {
          // High-surrogate alone at end of string
          codepoint = (int) c1;
        }
      } else {
        // Not a surrogate pair
        codepoint = (int) c1;
        if (i+1 < n) {
          char c2 = nonascii.charAt(i+1);
          int copepoint2 = (int) c2;
          if (copepoint2 == 65039) {
            // Surrogate pair
            codepoint = Character.toCodePoint(c1, c2);
            character += c2;
            i++;
          } else {
            // High-surrogate alone
            codepoint = (int) c1;
          }
        }
      }

      if(!character.isEmpty()) {
//        String fullhex = "";
//        for(int j = 0; j < character.length(); j++) {
//          String hex = "\\" + "u" + String.format("%x", (int) character.charAt(j));
////          String hex = Integer.toHexString((int) character.charAt(j));
////          while (hex.length() < 4) {
////            hex = "0" + hex;
////          }
////          hex = "\\u" + hex;
//          fullhex += hex;
//        }
//        wordbag.add(fullhex);
//        nonAsciiTokens += fullhex + " ";
        
        wordbag.add(character);
        nonAsciiTokens += character + " ";
      }
    }
  }
  
  public boolean isEmpty() {
    return wordbag.isEmpty();
  }
  
  public String getNonAscii() {
    return nonAsciiTokens.trim();
  }
  
  public String getContent() {
    return this.content;
  }
  
  @Override
  public String toString() {
    return wordbag.toString();
  }
  
  public JSONArray toJsonArray() throws JSONException {
    JSONArray array = new JSONArray();
    for(Object unicode: wordbag.uniqueSet()) {
      String unicodeString = (String) unicode;
      JSONObject object = new JSONObject();
      object.put("character", unicodeString);
      object.put("occurences", wordbag.getCount(unicode));
      array.put(object);
    }
    
    return array;
  }
}
