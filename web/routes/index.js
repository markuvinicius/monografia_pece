const express = require('express');
const mongoose = require('mongoose');
const { body, validationResult } = require('express-validator/check');
const router = express.Router();
const querystring = require('querystring'); 

const Registration = mongoose.model('Registration');
const Tweet = mongoose.model('Tweet');

router.get('/', (req, res) => {
    res.render('form', { title: 'Registration form' });
});

router.post('/',
  [
    body('name')
      .isLength({ min: 1 })
      .withMessage('Por favor, informe seu nome'),
    body('email')
      .isLength({ min: 1 })
      .withMessage('Por favor, informe seu e-mail'),
  ],
  (req, res) => {
    const errors = validationResult(req);

    if (errors.isEmpty()) {
        const registration = new Registration(req.body);
        var datetime = new Date();
        registration.data = datetime;
        registration.save()
            .then((reg) => {        
              const query = querystring.stringify({                
                "logged_user":reg.id
              });
              
              res.redirect('/unlabeled?' + query)              
            })
            .catch(() => { res.send('Sorry! Something went wrong.'); });
    } else {
      res.render('form', {
        title: 'Registration form',
        errors: errors.array(),
        data: req.body,
      });
    }
  }
);

router.get('/index', (req,res) => {
  res.render('index', {title:'Portal de Treinamento Supervisionado'});
});

router.get('/unlabeled', (req,res) => {            
    Tweet.find({"label":null}).limit(5)
      .then((tweets) => {        
        res.render('unlabeled', {title: 'Unlabeled Tweets', tweets:tweets, user:req.query.logged_user});
      })
      .catch(() => { res.send('Sorry! Something went wrong.'); });
});

router.post('/save', (req, res) => {    
    var logged_user = req.body['usuario_update']
    delete req.body['usuario_update']    

    for(var attributename in req.body){      
      var id = attributename
      var label = req.body[attributename]            

      Tweet.findByIdAndUpdate(id, 
        {
          "label": label,
          "labeled_by": logged_user
        },
        (err, todo) => {
          // Handle any possible database errors
          if (err) 
            return res.status(500).send(err);          
        })
      
    }
    const query = querystring.stringify({                
      "logged_user":logged_user
    });
    res.redirect('/unlabeled?' + query)    
               
});

module.exports = router;