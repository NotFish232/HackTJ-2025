const ALPHAMISSENSE_API_URL = "https://alphamissense.hegelab.org/hotspotapi";

$(function() {
    $("#alphamissense-submit").click(function() {
        let residueNum = $("#alphamissense-input").val();
        let parts = window.location.href.split("/");
        let uniprotId = parts[parts.length - 1];
        getAlphaMissenseResult(uniprotId, residueNum).then(results => {
            console.log(results);
            if (results) {
                $("#alphamissense-benign").text(results.benign);
                $("#alphamissense-pathogenic").text(results.pathogenic);
                $("#alphamissense-ambiguous").text(results.ambiguous);
            }
        });
    });
});

async function getAlphaMissenseResult(uniprotId, residueNum) {
    const url = `/alphamissense/${uniprotId}/${residueNum}`;
    try {
        const response = await axios.get(url, { timeout: 10000 });
        if (response.status !== 200) {
            return null;
        }
        const rJson = response.data;
        return {
            benign: rJson.benign,
            pathogenic: rJson.pathogenic,
            ambiguous: rJson.ambiguous,
        };
    } catch (error) {
        console.error(error);
        return null;
    }
}