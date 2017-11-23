/*global $:false, jQuery:false, Mustache:false */
var imageTemplate = "";
var lastQuery = "";
var lastQueryPage = 1;

function loadImageTemplate() {
    imageTemplate = $("#template").html();
    Mustache.parse(imageTemplate);
}

function doSearch(query) {
    $("#images").html("");
    $("#results").addClass("loading");
    $("#search-results-header").hide();
    $(".load-prev-page").hide();
    $(".load-more-results").hide();

    query = "any,contains," + query;
    var data = {
        query: query,
        json: true,
        indx: 1,
        bulkSize: 9
    };
    var url = "http://primo.nli.org.il/PrimoWebServices/xservice/search/brief?institution=NNL&loc=local,scope:(NNL)&query=lsr08,exact,%D7%94%D7%A1%D7%A4%D7%A8%D7%99%D7%99%D7%94+%D7%94%D7%9C%D7%90%D7%95%D7%9E%D7%99%D7%AA+%D7%90%D7%A8%D7%9B%D7%99%D7%95%D7%9F+%D7%93%D7%9F+%D7%94%D7%93%D7%A0%D7%99";
    $.ajax({
        type: "GET",
        url: url,
        data: data,
        jsonp: "callback",
        dataType: 'jsonp',
        success: function (response) {
            var totalHits = response.SEGMENTS.JAGROOT.RESULT.DOCSET['@TOTALHITS']
            var renderedResults = "";

            if (response.SEGMENTS.JAGROOT.RESULT.DOCSET.DOC && response.SEGMENTS.JAGROOT.RESULT.DOCSET.DOC.length) {
                var docs = response.SEGMENTS.JAGROOT.RESULT.DOCSET.DOC;
                var recordIds = docs.map(function (imageData) {
                    return imageData.PrimoNMBib.record.control.recordid;
                });

                var presentationAPIPrefix = "http://iiif.nli.org.il/IIIFv21/DOCID/";
                var presentationAPISuffix = "/manifest";
                var presentationAPIURLs = recordIds.map(function (recordId) {
                    return presentationAPIPrefix + recordId + presentationAPISuffix;
                });

                presentationAPIURLs.forEach(function (recordUrl) {
                    $.ajax({
                        type: "GET",
                        url: recordUrl,
                        success: function (response) {
                            let imageUrl = response.sequences[0].canvases[0].images[0].resource.service["@id"];
                            var fullImageURL = imageUrl + '/full/576,/0/default.jpg';
                            renderedResults = Mustache.render(imageTemplate, {picture: fullImageURL});

                            $("#images").append(renderedResults);
                        }
                    });
                });

                $("#images").on("click", ".pic" ,function(e){
                    var urlToFetch = e.target.src;
                    var backednURL = "http://34.239.198.2:5000/photo";
                    console.log(urlToFetch);

                    $.ajax({
                        type: "GET",
                        url: backednURL,
                        data: {
                            image_url: urlToFetch
                        },
                        jsonp: "callback",
                        dataType: 'jsonp',
                        success: function (response) {
                            console.log(response);
                            let preview = $("#preview").html('');
                            // let parent = $(e.target).parent();
                            var urlAfter = response.processed_image;
                            //"http://iiif.nli.org.il/IIIFv21/FL45931741/full/576,/0/default.jpg";
                            preview.append("<img src='"+urlToFetch+"'>");
                            preview.append("<img src='"+urlAfter+"'>");

                            $.fancybox.defaults.modal = true;
                            $.fancybox.open(preview);
                            preview.twentytwenty();
                            // setTimeout(function(){
                            //     let preview = $("#preview");
                            //     preview.twentytwenty();
                            // }, 1000);
                        }
                    });
                });



                $("#page-number").html(lastQueryPage);
                $("#search-results-header").show();
                if (docs.length >= 25) {
                    $(".load-more-results").show();
                }
                if (lastQueryPage > 1) {
                    $(".load-prev-page").show();
                }
            }
            else {
                renderedResults = "No results, please review your search or try a different one";
            }
            // $("#docs").hide().html(renderedResults).slideDown(700);
            $("#results").removeClass("loading");
        }
    });
}

$(document).ready(function () {
    loadImageTemplate();

    $("#ImagesSearch").keypress(function (e) {
        if (e.which === 13) {
            lastQuery = e.target.value;
            doSearch(lastQuery);
        }
    });

    $(".load-more-results").click(function (e) {
        lastQueryPage++;
        doSearch(lastQuery, lastQueryPage);
    });

    $(".load-prev-page").click(function (e) {
        if (lastQueryPage > 1) {
            lastQueryPage--;
            doSearch(lastQuery, lastQueryPage);
        }
    });
});
