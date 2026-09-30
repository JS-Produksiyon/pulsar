function extractI18n() {
    let out = {
      "placeholders": {},
      "strings": {},
      "titles": {}
    }

    Object.keys(out).forEach(key => {
        let src = "";
        switch (key) {
            case "placeholders":
                src = "i18n-placeholder";
                break;

            case "strings":
                src = "i18n";
                break;

            case "titles":
                src = "i18n-title";
                break;
        }

        $(`[data-${src}]`).each(function () {
            let strKey = $(this).data(src)
            let strData = "";
            switch (key) {
                case "placeholders":
                    strData = $(this).attr("placeholder");
                    break;
                
                case "strings":
                    strData = $(this).text()
                    break;

                case "titles":
                    strData = $(this).attr("title");
                    break;
            }

            out[key][strKey] = strData;
        })
    });

    console.log(out);
}
