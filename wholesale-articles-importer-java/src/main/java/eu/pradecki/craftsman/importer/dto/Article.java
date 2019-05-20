package eu.pradecki.craftsman.importer.dto;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.LinkedList;
import java.util.List;

@Data
// Use these fields on deserialization but ignore them on serialisation
@JsonIgnoreProperties(value = {"linenumber", "text"}, allowSetters = true)
public class Article {

    // articles
    @JsonIgnore
    private String recordType;
    private String articleId;
    private String articleName;
    private String inStock;

    // dimentions.da
    private List<String> alternativeArticleId = new LinkedList<>();

    // dimentions.dc
    private List<String> color = new LinkedList<>();

    // dimentions.pc
    private List<String> producingCompany = new LinkedList<>();

    // dimentions.pu
    private List<String> packagingUnitSize = new LinkedList<>();

    // prices
    private String listPrice;
    private String retailPrice;

    // texts
    private List<String> linenumber = new LinkedList<>();
    private List<String> text = new LinkedList<>();
    private List<Text> texts = new LinkedList<>();

    @AllArgsConstructor
    @NoArgsConstructor
    @Data
    public static class Text {
        private String linenumber;
        private String text;
    }

}
