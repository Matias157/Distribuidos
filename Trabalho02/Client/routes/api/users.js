var express = require("express");

var router = express.Router();

router.get("/", function(req, res, next){

    console.log("Users page - Return users as JSON file");
    res.json("JSON for users API");

});

// Exporta Router para o NodeJS se comunicar com outros arquivos
module.exports = router;