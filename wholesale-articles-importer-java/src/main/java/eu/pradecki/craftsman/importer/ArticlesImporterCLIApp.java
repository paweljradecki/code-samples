package eu.pradecki.craftsman.importer;

import com.fasterxml.jackson.core.JsonFactory;
import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.core.util.DefaultPrettyPrinter;
import com.fasterxml.jackson.databind.MappingIterator;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.dataformat.csv.CsvMapper;
import com.fasterxml.jackson.dataformat.csv.CsvParser;
import com.fasterxml.jackson.dataformat.csv.CsvSchema;
import eu.pradecki.craftsman.importer.dto.Article;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.LinkedList;
import java.util.List;

public class ArticlesImporterCLIApp {

    private static final char CSV_COLUMN_SEPARATOR = ';';
    private static final boolean IGNORE_CSV_COMMENTS = true;
    private static final CsvMapper CSV_MAPPER = new CsvMapper();
    private static final JsonFactory JSON_FACTORY = new JsonFactory();
    private static final ObjectMapper jsonMapper = new ObjectMapper();

    private static final Logger LOG
        = LoggerFactory.getLogger(ArticlesImporterCLIApp.class);
    private static final String ARTICLE_JSON_DIRPATH = "./article.json/";

    public static void main(String[] args) throws Exception {
       new ArticlesImporterCLIApp().run();
    }

    private void run() throws Exception {
        parseAll();
        mergeAllIntoOne();
    }

    private void parseAll() throws Exception {
        parseCsvToJson(
            "./data/articles.dat",
            new ArrayList<>(Arrays.asList(
                "recordType", "articleId", "articleName", "inStock"
            )),
            null
        );

        parseCsvToJson(
            "./data/dimensions_da.dat",
            new ArrayList<>(Arrays.asList(
                "recordType", "articleId", "alternativeArticleId"
            )),
            new ArrayList<>(Collections.singletonList(
                "alternativeArticleId"
            ))
        );

        parseCsvToJson(
            "./data/dimensions_dc.dat",
            new ArrayList<>(Arrays.asList(
                "recordType", "articleId", "color"
            )),
            new ArrayList<>(Collections.singletonList(
                "color"
            ))
        );

        parseCsvToJson(
            "./data/dimensions_dp.dat",
            new ArrayList<>(Arrays.asList(
                "recordType", "articleId", "producingCompany"
            )),
            new ArrayList<>(Collections.singletonList(
                "producingCompany"
            ))
        );

        parseCsvToJson(
            "./data/dimensions_du.dat",
            new ArrayList<>(Arrays.asList(
                "recordType", "articleId", "packagingUnitSize"
            )),
            new ArrayList<>(Collections.singletonList(
                "packagingUnitSize"
            ))
        );

        parseCsvToJson(
            "./data/prices.dat",
            new ArrayList<>(Arrays.asList(
                "recordType", "articleId", "listPrice", "retailPrice"
            )),
            new ArrayList<>(Arrays.asList(
                "listPrice", "retailPrice"
            ))
        );

        parseCsvToJson(
            "./data/texts.dat",
            new ArrayList<>(Arrays.asList(
                "recordType", "articleId", "linenumber", "text"
            )),
            new ArrayList<>(Arrays.asList(
                "linenumber", "text"
            ))
        );
    }

    private void parseCsvToJson(
        String pathname, List<String> columnNames, List<String> mergeAttributes
    ) throws IOException, NoSuchFieldException, IllegalAccessException {

        LOG.info("Parsing file: {}...", pathname);

        final MappingIterator<Article> csvIterator
            = readCsv(pathname, columnNames);

        while (csvIterator.hasNextValue()) {
            final Article newArticleData;
            try {
                newArticleData = csvIterator.nextValue();
            } catch (IOException e) {
                LOG.error(
                    "Incorrect data in file: {} in line: {} ",
                    pathname, csvIterator.getCurrentLocation().getLineNr()
                );
                LOG.error("Exception thrown: ", e);
                continue;
            }

            LOG.debug("New article: {}", newArticleData);
            if (newArticleData.getArticleId() == null
                || newArticleData.getArticleId().isBlank()) {
                LOG.error(
                    "Incorrect data in file {} in line: {}. No articleId. ",
                    pathname, csvIterator.getCurrentLocation().getLineNr()
                );
                continue;
            }

            final var mergedArticle
                = mergeNewWithCurrent(mergeAttributes, newArticleData);

            if (newArticleData.getText() != null && newArticleData.getText().size() > 0
            && newArticleData.getLinenumber() != null && newArticleData.getLinenumber().size() > 0
            ) {
                mergedArticle.getTexts().add(
                    new Article.Text(
                        newArticleData.getLinenumber().get(0), newArticleData.getText().get(0)
                    )
                );
            }

            LOG.debug("Current article: {}", mergedArticle);
            writeJsonToFile(mergedArticle,
                String.format("./article.json/%s.json", mergedArticle.getArticleId()),
                false
            );

        }
    }

    private void mergeAllIntoOne() throws IOException {
        final var articles = new ArrayList<>();
        final List<String> jsonArticlePaths = new LinkedList<>();

        try (var paths = Files.walk(Paths.get("./article.json"))) {
            paths
                .filter(Files::isRegularFile)
                .forEach(path -> jsonArticlePaths.add(path.toString()));
        }

        for (String path : jsonArticlePaths) {
            final var jsonFactory = new JsonFactory();
            final var jp = jsonFactory.createParser(new File(path));
            jp.setCodec(new ObjectMapper());
            final Article article = jp.readValueAs(Article.class);
            articles.add(article);
        }

        writeJsonToFile(articles, "./final-json-output/articles.json");
    }

    private Article mergeNewWithCurrent(
        List<String> updateAttributes, Article newArticleData
    ) throws IOException, IllegalAccessException, NoSuchFieldException {

        Article currentArticleData;
        if (updateAttributes != null && !updateAttributes.isEmpty()) {

            final var jp = JSON_FACTORY.createParser(new File(ARTICLE_JSON_DIRPATH + newArticleData.getArticleId() + ".json"));
            jp.setCodec(jsonMapper);
            currentArticleData = jp.readValueAs(Article.class);
            LOG.debug("Current article read from file: {}", currentArticleData);

            for (var attr : updateAttributes) {
                LOG.debug("UpdateAttribute: {}", attr);

                final var currentAttrField = currentArticleData.getClass().getDeclaredField(attr);
                currentAttrField.setAccessible(true);
                final var currentAttrValue = currentAttrField.get(currentArticleData);
                final var newAttrField = newArticleData.getClass().getDeclaredField(attr);
                newAttrField.setAccessible(true);
                final var newAttrValue = newAttrField.get(newArticleData);
                if (currentAttrValue != null && !currentAttrValue.equals(newAttrValue)) {

                    if (currentArticleData.getClass().getDeclaredField(attr).getType().equals(List.class)) {
                        final List curList = (List) currentAttrValue;
                        final List newList = (List) newAttrValue;
                        curList.addAll(newList);
                    } else {

                        LOG.error(
                            "Merge conflict! Article Json with articleId: {}. Its attribute: {} already has a value: {}. " +
                                "Skipping and will not override it with value: {}",
                            currentArticleData.getArticleId(),
                            currentAttrField.getName(), currentAttrValue,
                            newAttrValue
                        );
                    }
                } else {
                    currentAttrField
                        .set(
                            currentArticleData,
                            newAttrValue
                        );
                }
            }
        } else {
            currentArticleData = newArticleData;
        }
        return currentArticleData;
    }

    private MappingIterator<Article> readCsv(String pathname, List<String> columnNames) throws IOException {
        final var schemaBuilder
            = CsvSchema.builder()
                .setColumnSeparator(CSV_COLUMN_SEPARATOR)
                .setAllowComments(IGNORE_CSV_COMMENTS);

        for (String columnName : columnNames) {
            schemaBuilder.addColumn(columnName);
        }
        final var schema = schemaBuilder.build();

        final var csvFile = new File(pathname);
        return CSV_MAPPER
            .enable(CsvParser.Feature.IGNORE_TRAILING_UNMAPPABLE)
            .enable(JsonGenerator.Feature.IGNORE_UNKNOWN)
            .readerFor(Article.class)
            .with(schema)
            .readValues(csvFile);
    }

    private void writeJsonToFile(Object jsonObject, String pathname) throws IOException {
        writeJsonToFile(jsonObject, pathname, true);
    }

    private void writeJsonToFile(Object jsonObject, String pathname, boolean stdoutPreview) throws IOException {
        final var writer = jsonMapper.writer(new DefaultPrettyPrinter());
        LOG.debug("jsonObject: {}", jsonObject);
        writer.writeValue(new File(pathname), jsonObject);
        if (stdoutPreview) {
            final var json = jsonMapper.writeValueAsString(jsonObject);
            LOG.info("{}: {}", pathname, json);
        }
    }
}
