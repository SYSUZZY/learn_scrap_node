var express = require('express');

var app = express();

var handlebars = require('express3-handlebars')
				.create({defaultLayout:'main'});
app.engine('handlebars',handlebars.engine);
app.set('view engine','handlebars');
app.use(require('body-parser')())
app.set('port',process.env.PORT || 3000);

app.get('/headers',function(req,res){
	res.set('content-Type','text/plain');
	var s = '';
	for (var name in req.headers) s+= name + ': ' + req.headers[name] + '\n';
	res.send(s);                             
});
app.get('/',function(req,res){
	res.render('home',{layout:null});
});
app
app.get('/about',function(req,res){
	res.render('about');
});
app.get('/newsletter',function(req,res){
	 res.render('newsletter',{ csrf:'CSRF token goes here' });
});
app.get('/thank-you',function(req,res){
	res.render('thank-you');
});
app.post("/process",function(req,res){
	console.log('Form(from querystring:'+req.query.form);
	console.log('csrf token(from hidden form field'+req.body._csrf);
	console.log('Name(from visible form field'+req.body.name);
	console.log('Email (from visible form field'+req.body.email);
	res.redirect(303,'/thank-you')
});
app.use(function(req,res){
	res.status(404);
	res.render('404');
});
app.use(function(err,req,res,next){
	console.log(err.stack);
	res.status(500);
	res.render('500');
});
app.listen(app.get('port'),function(){
	console.log('started on http://localhost:'+app.get('port'));
});