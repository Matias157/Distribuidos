// ------------------------------
// Trabalho 2 - Sistemas Distribuídos
// Autores: 
// Alexandre Herrero matias
// Matheus Fonseca Alexandre de Oliveira
// Professor: Ana Cristina Vendramin
// Projeto: Doodle
// ------------------------------

// Libraries

var express = require("express");
var bodyParser = require("body-parser");
const request = require('request');
const https = require('https');
const http = require('http');
var flash = require('connect-flash');

var urlencodedParser = bodyParser.urlencoded({ extended: false });

var router = express.Router();
var username;

// Heads to Starter Page
// LOGIN Submit -
router.get("/", function (req, res, next) {

    console.log("Starter page");
    res.render("home/index", {hasUsername: false});

});

// Heads to HOME Page
// Goes to three main menus
router.get("/home", function (req, res, next) {

    console.log("Home button");
    res.render("home/home", {hasUsername: true, username: username});

});

// Heads to Create New Survey Page
router.get("/newSurvey", function (req, res) {

    res.render("home/newSurvey", {hasUsername: true, username: username});
});

// HTTP POST New Survey on server.
router.post('/newSurveyPost', urlencodedParser, function (req, res) {
    req.body.creator = username;
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

    const req1 = http.request(options, resp => {
        console.log(`statusCode: ${resp.statusCode}`)

        resp.on('data', d => {
            process.stdout.write(d);
            res.render("home/home", {hasUsername: true, username: username});
        });
    });

    req1.on('error', error => {
        console.error(error)
    });

    req1.write(data);
    req1.end();
});

// Heads to consult surveys
router.get("/consultSurvey", function (req, res) {

    // Load the page with Submit button
    res.render("home/consultSurvey", {firstPage: true, hasUsername: true, username: username});

});

// HTTP GET All Open surveys available.
router.get("/voteSurvey", function (req, res) {

    const options = {
        hostname: 'localhost',
        port: 5000,
        path: '/survey/info',
        method: 'GET'
    }

    var data;

    console.log(data);

    req = http.request(options, resp => {
        console.log(`statusCode: ${resp.statusCode}`)

        resp.on('data', d => {
            data = d.toString('utf8');
            console.log(data);
            data = data.replace(/(?:\r\n|\r|\n)/g, "<br />");
            res.render("home/voteSurvey", {voteSurveyDetails: true, list: data, hasUsername: true, username: username});
        })
    })

    req.on('error', error => {
        res.render("home/voteSurvey", {voteSurveyDetails: false, hasUsername: true, username: username});
    })

    req.end()
});

// HTTP POST Send Vote option to server.
router.post("/voteSurveyPost", urlencodedParser, function(req, res){
    req.body.name = username;
    console.log(req.body);

    const options = {
        hostname: 'localhost',
        port: 5000,
        path: '/survey/vote',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    }

    const data = JSON.stringify(req.body);

    console.log(data);

    const req1 = http.request(options, resp => {
        console.log(`statusCode: ${resp.statusCode}`)

        resp.on('data', d => {
            process.stdout.write(d);
            res.redirect("/voteSurvey");
            
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
        path: '/survey/consult?survey=' + req.query.survey + '&name=' + username,
        method: 'GET'
    }

    var data;

    req = http.request(options, resp => {
        console.log(`statusCode: ${resp.statusCode}`)

        resp.on('data', d => {
            data = d.toString('utf8');
            console.log(data);
            data = data.replace(/(?:\r\n|\r|\n)/g, "<br />");
            res.render("home/consultSurvey", {firstPage: false, surveyDetail: data, hasUsername: true, username: username});
        })
    })

    req.on('error', error => {
        res.render("home/consultSurvey", {firstPage: true, hasUsername: true, username: username});
    })

    req.end()
});

// Login the user, redirect to home page for logged user.
router.post("/login", urlencodedParser, function (req, res, next) {
    username = req.body.name;

    const options = {
        hostname: 'localhost',
        port: 5000,
        path: '/user',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    }

    const data = JSON.stringify(req.body);

    console.log(data);

    const req1 = http.request(options, resp => {
        console.log(`statusCode: ${resp.statusCode}`)

        resp.on('data', d => {
            process.stdout.write(d);
            res.render("home/home", {hasUsername: true, username: username});
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