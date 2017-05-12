/**
 * Created by GGC on 2017/4/28.
 */
var sliderplayer=function (imgurl,id,w,h,loadedCallback) {
    this._turns=1;
    this._speed = 1000 / 10;
    this.loopTimer = null;
    this.canvasObj = null;
    this.context = null;
    this.imageList = [];
    this.animateList = [];
    this.animateAction = 0;
    this.animateCurframe = 0;
	
	this.w=w;
	this.h=h;
	this.imgurl=imgurl;
	this.id=id;
	this.loadedCallback=loadedCallback;
	
	that=this;
    this.main();
}
sliderplayer.prototype.main=function() {
	this._setCanvas();
	this._loadResource({
		'id': this.id,
		'src': this.imgurl
	});
}

sliderplayer.prototype._setCanvas=function() {
	var object = document.getElementById(this.id);
	object.innerHTML = '<canvas id="' + this.id + '_slideplayer" width="' + this.w +'" height="'+this.h+'" style="margin: 0 auto;"></canvas>';

	canvasObj = document.getElementById(this.id + "_slideplayer");
	this.context = canvasObj.getContext("2d");
}

sliderplayer.prototype._loadResource=function(item){
	var that=this;
	var image = new Image();
	image.src = item.src;
	image.onload = function() {
		that.imageList[item.id] = image;

		that.animateList = that._divideCoordinate(image.width,image.height, image.height/that.h,image.width/that.w);
		//loop();
		if(typeof that.loadedCallback=="function")
			that.loadedCallback();
	}
	
}
sliderplayer.prototype.stopautoplay=function(){
	if (this.loopTimer) {
		clearInterval(this.loopTimer);
	}
}
sliderplayer.prototype._loop=function() {
	var that=this;
	if (this.loopTimer) {
		clearInterval(this.loopTimer);
	}
	this.loopTimer = setInterval(function() {
		that.context.fillRect(0, 0, that.w, that.h);
		that._draw(that.context, that.imageList[that.id], that.animateList);
	}, this._speed)
}
sliderplayer.prototype.slideplay=function(autoplay){
	this.stopautoplay();
	this.context.fillRect(0,0, this.w, this.h);
	this._draw(this.context, this.imageList[this.id], this.animateList);
}
sliderplayer.prototype.autoplay=function() {
	this._loop();
}

sliderplayer.prototype._divideCoordinate=function(w, h, row, col) {
	var i, j, cw = w / col, ch = h / row, r = [], c;
	for (i = 0; i < row; i++) {
		c = [];
		for (j = 0; j < col; j++) {
			c.push({x : cw * j, y : ch * i, width : cw, height : ch});
		}
		r.push(c);
	}
	return r;
};

sliderplayer.prototype._draw=function(c, bitmapData, list) {
	//console.log(list);
	if(this.animateCurframe > list[this.animateAction].length-1){ //当前图片位置大于当前行图片数量
		this.animateAction+=1;	//当前行下移一行
		if(this.animateAction > list.length-1){//如果正序已经播放完
			this.animateAction = 0;
		}
		this.animateCurframe = 0; //当前图片位置移动到上一行行首
		//console.log("fuzhi");
	}else if(this.animateCurframe<0){
		//console.log("====");
		this.animateAction-=1;	//当前行上移一行
		if(this.animateAction <0){	//如果是倒序播放完
			this.animateAction = list.length-1;
		}
		this.animateCurframe= list[this.animateAction].length-1;
	}
	//console.log("col",animateCurframe,"row",animateAction);
	var p = list[this.animateAction][this.animateCurframe];
	c.drawImage(
		bitmapData,
		p.x,
		p.y,
		p.width,
		p.height,
		(this.w - p.width)/2,
		(this.h - p.height)/3,
		p.width,
		p.height
	);

	this.animateCurframe +=(this._turns)*1;
}