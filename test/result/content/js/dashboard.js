/*
   Licensed to the Apache Software Foundation (ASF) under one or more
   contributor license agreements.  See the NOTICE file distributed with
   this work for additional information regarding copyright ownership.
   The ASF licenses this file to You under the Apache License, Version 2.0
   (the "License"); you may not use this file except in compliance with
   the License.  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/
var showControllersOnly = false;
var seriesFilter = "";
var filtersOnlySampleSeries = true;

/*
 * Add header in statistics table to group metrics by category
 * format
 *
 */
function summaryTableHeader(header) {
    var newRow = header.insertRow(-1);
    newRow.className = "tablesorter-no-sort";
    var cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Requests";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 3;
    cell.innerHTML = "Executions";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 7;
    cell.innerHTML = "Response Times (ms)";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Throughput";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 2;
    cell.innerHTML = "Network (KB/sec)";
    newRow.appendChild(cell);
}

/*
 * Populates the table identified by id parameter with the specified data and
 * format
 *
 */
function createTable(table, info, formatter, defaultSorts, seriesIndex, headerCreator) {
    var tableRef = table[0];

    // Create header and populate it with data.titles array
    var header = tableRef.createTHead();

    // Call callback is available
    if(headerCreator) {
        headerCreator(header);
    }

    var newRow = header.insertRow(-1);
    for (var index = 0; index < info.titles.length; index++) {
        var cell = document.createElement('th');
        cell.innerHTML = info.titles[index];
        newRow.appendChild(cell);
    }

    var tBody;

    // Create overall body if defined
    if(info.overall){
        tBody = document.createElement('tbody');
        tBody.className = "tablesorter-no-sort";
        tableRef.appendChild(tBody);
        var newRow = tBody.insertRow(-1);
        var data = info.overall.data;
        for(var index=0;index < data.length; index++){
            var cell = newRow.insertCell(-1);
            cell.innerHTML = formatter ? formatter(index, data[index]): data[index];
        }
    }

    // Create regular body
    tBody = document.createElement('tbody');
    tableRef.appendChild(tBody);

    var regexp;
    if(seriesFilter) {
        regexp = new RegExp(seriesFilter, 'i');
    }
    // Populate body with data.items array
    for(var index=0; index < info.items.length; index++){
        var item = info.items[index];
        if((!regexp || filtersOnlySampleSeries && !info.supportsControllersDiscrimination || regexp.test(item.data[seriesIndex]))
                &&
                (!showControllersOnly || !info.supportsControllersDiscrimination || item.isController)){
            if(item.data.length > 0) {
                var newRow = tBody.insertRow(-1);
                for(var col=0; col < item.data.length; col++){
                    var cell = newRow.insertCell(-1);
                    cell.innerHTML = formatter ? formatter(col, item.data[col]) : item.data[col];
                }
            }
        }
    }

    // Add support of columns sort
    table.tablesorter({sortList : defaultSorts});
}

$(document).ready(function() {

    // Customize table sorter default options
    $.extend( $.tablesorter.defaults, {
        theme: 'blue',
        cssInfoBlock: "tablesorter-no-sort",
        widthFixed: true,
        widgets: ['zebra']
    });

    var data = {"OkPercent": 100.0, "KoPercent": 0.0};
    var dataset = [
        {
            "label" : "FAIL",
            "data" : data.KoPercent,
            "color" : "#FF6347"
        },
        {
            "label" : "PASS",
            "data" : data.OkPercent,
            "color" : "#9ACD32"
        }];
    $.plot($("#flot-requests-summary"), dataset, {
        series : {
            pie : {
                show : true,
                radius : 1,
                label : {
                    show : true,
                    radius : 3 / 4,
                    formatter : function(label, series) {
                        return '<div style="font-size:8pt;text-align:center;padding:2px;color:white;">'
                            + label
                            + '<br/>'
                            + Math.round10(series.percent, -2)
                            + '%</div>';
                    },
                    background : {
                        opacity : 0.5,
                        color : '#000'
                    }
                }
            }
        },
        legend : {
            show : true
        }
    });

    // Creates APDEX table
    createTable($("#apdexTable"), {"supportsControllersDiscrimination": true, "overall": {"data": [1.0, 500, 1500, "Total"], "isController": false}, "titles": ["Apdex", "T (Toleration threshold)", "F (Frustration threshold)", "Label"], "items": [{"data": [1.0, 500, 1500, "11"], "isController": false}, {"data": [1.0, 500, 1500, "12"], "isController": false}, {"data": [1.0, 500, 1500, "13"], "isController": false}, {"data": [1.0, 500, 1500, "14"], "isController": false}, {"data": [1.0, 500, 1500, "15"], "isController": false}, {"data": [1.0, 500, 1500, "16"], "isController": false}, {"data": [1.0, 500, 1500, "17"], "isController": false}, {"data": [1.0, 500, 1500, "18"], "isController": false}, {"data": [1.0, 500, 1500, "19"], "isController": false}, {"data": [1.0, 500, 1500, "1"], "isController": false}, {"data": [1.0, 500, 1500, "2"], "isController": false}, {"data": [1.0, 500, 1500, "3"], "isController": false}, {"data": [1.0, 500, 1500, "4"], "isController": false}, {"data": [1.0, 500, 1500, "5"], "isController": false}, {"data": [1.0, 500, 1500, "Test"], "isController": true}, {"data": [1.0, 500, 1500, "6"], "isController": false}, {"data": [1.0, 500, 1500, "7"], "isController": false}, {"data": [1.0, 500, 1500, "8"], "isController": false}, {"data": [1.0, 500, 1500, "9"], "isController": false}, {"data": [1.0, 500, 1500, "10"], "isController": false}]}, function(index, item){
        switch(index){
            case 0:
                item = item.toFixed(3);
                break;
            case 1:
            case 2:
                item = formatDuration(item);
                break;
        }
        return item;
    }, [[0, 0]], 3);

    // Create statistics table
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 9648, 0, 0.0, 1.145211442786076, 0, 35, 1.0, 2.0, 3.0, 4.0, 325.24271844660194, 75.80085762624729, 140.0694615632585], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["11", 500, 0, 0.0, 0.9480000000000001, 0, 8, 1.0, 1.0, 1.0, 3.0, 87.22958827634334, 16.099992367411026, 38.07775972609909], "isController": false}, {"data": ["12", 500, 0, 0.0, 0.8859999999999997, 0, 4, 1.0, 1.0, 1.0, 2.0, 86.79048776254122, 16.018947448359658, 37.88608206040618], "isController": false}, {"data": ["13", 500, 0, 0.0, 0.9039999999999994, 0, 4, 1.0, 1.0, 1.0, 2.990000000000009, 82.02099737532808, 15.138641117125983, 35.80408772145669], "isController": false}, {"data": ["14", 500, 0, 0.0, 0.9259999999999999, 0, 9, 1.0, 1.0, 1.0, 2.990000000000009, 76.78132678132678, 14.171553478194104, 33.51684870239558], "isController": false}, {"data": ["15", 500, 0, 0.0, 0.9919999999999997, 0, 10, 1.0, 1.0, 1.0, 6.0, 80.0384184408516, 14.772715903633744, 34.938645549863935], "isController": false}, {"data": ["16", 500, 0, 0.0, 0.9140000000000001, 0, 7, 1.0, 1.0, 1.0, 2.0, 72.43227582210633, 13.368847783572361, 31.618386027813997], "isController": false}, {"data": ["17", 500, 0, 0.0, 0.9779999999999995, 0, 8, 1.0, 1.0, 1.0, 4.980000000000018, 72.34843003906816, 13.353372341195197, 31.581785378382293], "isController": false}, {"data": ["18", 491, 0, 0.0, 0.9164969450101838, 0, 7, 1.0, 1.0, 1.0, 3.0, 80.3863785199738, 14.836939004174853, 35.090538279715126], "isController": false}, {"data": ["19", 410, 0, 0.0, 0.9268292682926829, 0, 12, 1.0, 1.0, 1.0, 3.8899999999999864, 84.17162800246355, 15.535583684048449, 36.74288839560665], "isController": false}, {"data": ["1", 715, 0, 0.0, 3.0503496503496477, 0, 35, 3.0, 4.0, 4.0, 29.680000000000064, 24.119552017271623, 20.2331007644886, 8.620855506173257], "isController": false}, {"data": ["2", 529, 0, 0.0, 1.1871455576559553, 0, 6, 1.0, 2.0, 2.0, 4.0, 18.592717559398288, 3.4316636901623787, 8.116156981495148], "isController": false}, {"data": ["3", 502, 0, 0.0, 1.0856573705179295, 0, 8, 1.0, 1.0, 2.0, 3.0, 19.224141232336383, 3.5482057547964616, 8.391788213724965], "isController": false}, {"data": ["4", 501, 0, 0.0, 1.0079840319361284, 0, 7, 1.0, 1.0, 2.0, 2.0, 19.540543702952533, 3.6066042576738564, 8.529905307831818], "isController": false}, {"data": ["5", 500, 0, 0.0, 1.0979999999999999, 0, 14, 1.0, 1.0, 2.0, 2.0, 112.71415689810641, 20.80368716185753, 49.20237122407575], "isController": false}, {"data": ["Test", 491, 0, 0.0, 21.635437881873713, 14, 52, 21.0, 25.0, 28.399999999999977, 47.15999999999997, 297.0356926799758, 1226.9606870084694, 2418.7113628629763], "isController": true}, {"data": ["6", 500, 0, 0.0, 1.0700000000000003, 0, 4, 1.0, 2.0, 2.0, 2.0, 107.34220695577501, 19.812184682267066, 46.85738916917131], "isController": false}, {"data": ["7", 500, 0, 0.0, 1.0960000000000003, 0, 9, 1.0, 2.0, 2.0, 4.0, 91.50805270863836, 16.889669884699853, 39.945409727306], "isController": false}, {"data": ["8", 500, 0, 0.0, 1.0299999999999991, 0, 9, 1.0, 1.0, 2.0, 5.990000000000009, 94.32182607055273, 17.409008913412563, 41.17368774759479], "isController": false}, {"data": ["9", 500, 0, 0.0, 0.9959999999999993, 0, 11, 1.0, 1.0, 1.0, 6.0, 87.56567425569177, 16.162023861646233, 38.224469133099824], "isController": false}, {"data": ["10", 500, 0, 0.0, 0.8819999999999998, 0, 6, 1.0, 1.0, 1.0, 2.0, 90.57971014492753, 16.718325407608695, 39.5401664402174], "isController": false}]}, function(index, item){
        switch(index){
            // Errors pct
            case 3:
                item = item.toFixed(2) + '%';
                break;
            // Mean
            case 4:
            // Mean
            case 7:
            // Median
            case 8:
            // Percentile 1
            case 9:
            // Percentile 2
            case 10:
            // Percentile 3
            case 11:
            // Throughput
            case 12:
            // Kbytes/s
            case 13:
            // Sent Kbytes/s
                item = item.toFixed(2);
                break;
        }
        return item;
    }, [[0, 0]], 0, summaryTableHeader);

    // Create error table
    createTable($("#errorsTable"), {"supportsControllersDiscrimination": false, "titles": ["Type of error", "Number of errors", "% in errors", "% in all samples"], "items": []}, function(index, item){
        switch(index){
            case 2:
            case 3:
                item = item.toFixed(2) + '%';
                break;
        }
        return item;
    }, [[1, 1]]);

        // Create top5 errors by sampler
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 9648, 0, null, null, null, null, null, null, null, null, null, null], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
