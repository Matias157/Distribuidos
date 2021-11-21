var express = require("express");
var bodyParser = require("body-parser");
const request = require('request');
const https = require('https');
const http = require('http');

var urlencodedParser = bodyParser.urlencoded({ extended: false });

var router = express.Router();

// POST NEW SURVEY ON SERVER
router.post('/newSurveyPost', urlencodedParser, function (req, res) {
    console.log(req.body);

    const options = {
        hostname: 'localhost',
        port: 5000,
        path: '/survey',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    }

    const data = JSON.stringify(req.body);

    console.log(data);

    const req1 = http.request(options, res => {
        console.log(`statusCode: ${res.statusCode}`)

        res.on('data', d => {
            process.stdout.write(d)
        })
    })

    req1.on('error', error => {
        console.error(error)
    })

    req1.write(data)
    req1.end();


    //res.render('newSurveyPost', {});
});

// GET SURVEYS FROM SERVER
router.get('/consultSurveyPost', function (req, res, next) {
    
    request('https://www.google.com/', {json: true}, (err, res, body) => {
        if (err) { return console.log(err); }
        console.log(body.url);
        console.log(body.explanation);
      });

      

    // const options = {
    //     hostname: 'www.google.com',
    //     port: 80,
    //     path: '/index',
    //     method: 'GET'
    // }

    // const req1 = https.request(options, res => {
    //     console.log(`statusCode: ${res.statusCode}`)

    //     res.on('data', d => {
    //         process.stdout.write(d)
    //     })
    // })

    // req1.on('error', error => {
    //     console.error(error)
    // })

    // req1.end()
});


router.get("/", function (req, res, next) {

    console.log("Starter page");
    res.render("home/index");

});

router.get("/home", function (req, res, next) {

    console.log("Home button");
    res.render("home/home");

});

router.get("/newSurvey", function (req, res) {

    res.render("home/newSurvey");
});

router.get("/newSurveyPost", function (req, res, next) {

});

router.get("/consultSurvey", function (req, res) {

    res.render("home/consultSurvey");

});

router.get("/voteSurvey", function (req, res) {

    res.render("home/voteSurvey");

});


// Login the user, redirect to home page for logged user.
router.post("/login", function (req, res, next) {
    var username = req.body.username;

    // TODO: Connect to server and check for available username
    // TODO: Send to server as Json file?

    // If correct, redirect
});

// Exporta Router para o NodeJS se comunicar com outros arquivos
module.exports = router;