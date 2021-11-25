var express = require("express");

var router = express.Router();

router.use("/users", require("./users"));

// Exporta Router para o NodeJS se comunicar com outros arquivos
module.exports = router;