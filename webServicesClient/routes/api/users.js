var express = require("express");

var router = express.Router();

router.get("/", function(req, res, next){

    console.log("Users page");
    res.json("JSON for user API");

});

// Exporta Router para o NodeJS se comunicar com outros arquivos
module.exports = router;