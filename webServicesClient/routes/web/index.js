var express = require("express");

var router = express.Router();

router.use(function(req, res, next){
    // TODO: check this again. 
    res.locals.currentUser = req.user;

    next();
});

// TODO: Add in Error and Info
router.use("/", require("./home"));

module.exports = router;