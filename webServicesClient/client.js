const https = require('https')
var express = require("express");
var path = require("path");
var bodyParser = require("body-parser");
var session = require("express-session");
var flash = require("connect-flash");

var jsonParser = bodyParser.json();

var client = express();

// TODO: Connect with server here.
// use params.<> if necessary

client.set("port", process.env.PORT || 3000);

// Associando a pasta views, e associando a view ejs
client.set("views", path.join(__dirname, "views"));
client.set("view engine", "ejs");

client.use("/", require("./routes/web"));
client.use("/api", require("./routes/api"));
client.use(session({
    secret: "any198127381laskdhsl",
    cookie: { maxAge: 60000},
    resave: false,
    saveUninitialized: false
}));
client.use(flash());

client.listen(client.get("port"), function(){
    console.log("Server started on port " + client.get("port"))
});