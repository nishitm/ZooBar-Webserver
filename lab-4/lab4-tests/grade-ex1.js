var fs = require("fs");
var system = require("system");
var webpage = require("webpage");

var grading = require("./grading");

function findUrl(answerPath) {
    // People put random text. Find the first line that starts with
    // the right thing. open().readLine() would be nice, except their
    // API can't actually distinguish empty lines from EOF.
    var answerLines = fs.read(answerPath).split('\n');
    var prefix = "http://localhost:8080/zoobar/index.cgi/users?";
    var urls = answerLines.filter(function(url) {
        return url.substr(0, prefix.length) == prefix;
    });
    // Some students put the intended URL first and the unencoded or
    // (in one case) development URL second. Some in the other
    // order. Prefer the one with more %s. If a tie, prefer the
    // earlier.
    //
    // TODO(davidben): Ask students to place the URL in the first line
    // or something next year and make this less complicated.
    var bestUrl = undefined;
    var bestCount = -1;
    urls.forEach(function(url) {
        var m = url.match(/%/g);
        if (!m) return;
        var count = m.length;
        if (count > bestCount) {
            bestCount = count;
            bestUrl = url;
        }
    });
    return bestUrl;
}

function main(studentDir) {
    if (studentDir === undefined) {
        console.log("USAGE: phantomjs " + system.args[0] + " student_dir/");
        phantom.exit();
        return;
    }
    var answerPath = studentDir + "/answer-1.txt";
    var screenshotPath = studentDir + "/lab4-tests/answer-1.png";
    if (!fs.isFile(answerPath)) {
        console.log("FAIL - No answer-1.txt");
        phantom.exit();
        return;
    }

    var url = findUrl(answerPath);
    if (url === undefined) {
        console.log("Could not find URL. Please ensure your URL is the first line of answer-1.txt.");
        phantom.exit();
        return;
    }
    console.log("Found URL: " + url);

    grading.registerTimeout();

    // First login.
    grading.initUsers(function(auth) {
        phantom.cookies = auth.graderCookies;

    // clear the log file
    fs.write('/tmp/requests.log', '', 'w');

        // Print out the cookie we expect.
        //console.log("???? - Check your e-mail; the cookie is: " +
        //            grading.getCookie("localhost", "PyZoobarLogin"));

        // Now make a new page and open the attacker's URL.
        var page = webpage.create();
        grading.openOrDie(page, url, function() {
            // Wait 1s for any JS to settle and take a picture.
            setTimeout(function () {
                grading.derandomize(page);
		            page.render(screenshotPath);
                // check for cookie in the log file
                var data = fs.read('/tmp/requests.log');
                console.log(data);
                if (data.indexOf(encodeURIComponent(grading.getCookie("localhost", "PyZoobarLogin"))) > -1) {
                  console.log("\033[1;32mExercise 1 Passed!\033[m Found the cookie in logs");
                }
                else {
                  console.log("Test Failed! Could not find the cookie in logs")
                }
                phantom.exit();
            }, 1000);
        });
    });
}

main.apply(null, system.args.slice(1));
