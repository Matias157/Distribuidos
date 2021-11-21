var express = require("express");
var bodyParser = require("body-parser");
const request = require('request');
const https = require('https');
const http = require('http');

var urlencodedParser = bodyParser.urlencoded({ extended: false });

var router = express.Router();

// Heads to Starter Page
// LOGIN Submit -
router.get("/", function (req, res, next) {

    console.log("Starter page");
    res.render("home/index");

});

// Heads to HOME Page
// Goes to three main menus
router.get("/home", function (req, res, next) {

    console.log("Home button");
    res.render("home/home");

});

// Heads to Create New Survey Page
router.get("/newSurvey", function (req, res) {

    res.render("home/newSurvey");
});

// HTTP POST New Survey on server.
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

// Heads to consult surveys
router.get("/consultSurvey", function (req, res) {

    // Load the page with Submit button
    res.render("home/consultSurvey", {firstPage: true});

});

// HTTP GET All Open surveys available.
router.get("/voteSurvey", function (req, res) {

    const options = {
        hostname: 'localhost',
        port: 5000,
        path: '/survey/info',
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }

    const data = JSON.stringify(req.body);

    console.log(data);

    const req1 = http.request(options, res => {
        console.log(`statusCode: ${res.statusCode}`)

        res.on('data', d => {
            process.stdout.write(d);
        })
    })

    req1.on('error', error => {
        console.error(error);
    })

    req1.write(data);
    req1.end();

    if(data){
        res.render("home/voteSurvey", {voteSurveyDetails: true, list: data});
    }
    else{
        res.render("home/voteSurvey", {voteSurveyDetails: false});
    }
    
    
});

// HTTP POST Send Vote option to server.
router.get("/voteSurveyPost", function(req, res){
    console.log(req.body);

    const options = {
        hostname: 'localhost',
        port: 5000,
        path: '/survey', // TODO: Change to correct PATH
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

});

// HTTP GET Send Survey would like to consult to server
router.get("/getSurveyData", function (req, res) {

    const options = {
        hostname: 'localhost',
        port: 5000,
        path: '/survey/info', // TODO: Change here
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }

    const data = JSON.stringify(req.body);

    console.log(data);

    const req1 = http.request(options, res => {
        console.log(`statusCode: ${res.statusCode}`)

        res.on('data', d => {
            process.stdout.write(d);
        })
    })

    req1.on('error', error => {
        console.error(error);
    })

    req1.write(data);
    req1.end();

    if(data){
        res.render("home/consultSurvey", {firstPage: false, surveyDetail: data});
    }
    else{
        res.render("home/voteSurvey", {firstPage: true});
    }

    res.render("home/voteSurvey", {voteSurveyDetails: "You submited the button!"});
    
});



// Login the user, redirect to home page for logged user.
router.post("/login", function (req, res, next) {
    var username = req.body.username;

    // Se der certo preciso passar essa var pra const e universal.

    const options = {
        hostname: 'localhost',
        port: 5000,
        path: '/survey', // TODO: Change to correct PATH
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


});

// Exporta Router para o NodeJS se comunicar com outros arquivos
module.exports = router;