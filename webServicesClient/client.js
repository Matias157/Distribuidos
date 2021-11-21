const https = require('https')
var express = require("express");
var path = require("path");
var bodyParser = require("body-parser");

var jsonParser = bodyParser.json();

var client = express();

// TODO: Connect with server here.
// use params.<> if necessary

client.set("port", process.env.PORT || 3000);

// Associando a pasta views, e associando a view ejs
client.set("views", path.join(__dirname, "views"));
client.set("view engine", "ejs");

client.use("/", require("./routes/web"));

client.listen(client.get("port"), function(){
    console.log("Server started on port " + client.get("port"))
});