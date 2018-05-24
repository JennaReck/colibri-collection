$(document).ready(function() {

	$('#color-table td').click(function() {
        var checkBox = $('#checkbox-' + this.id);
        checkBox.prop("checked", !checkBox.prop("checked"));
        if(checkBox.is(':checked')){
            $(this).addClass("selected");
		}
        else {
            $(this).removeClass("selected");  
        }
    });
	$('#species-whole-overlay div').click(function(event) {
		toggleSpeciesOverlay(currentHumID);
		
	});
	$('#species-whole-overlay div img').click(function(event) {
		event.stopPropagation();
	});
	$('#select-hum-name-button').click(function() {
		window.location.href = document.getElementById('select-hum-name').value;
	});
	
	$('#slideshow-pause-play-button').click(function(){
		for(i=0;i<currentQueue.length-1;i=i+1){
				clearTimeout(currentQueue[i]);
			}
		currentQueue = [];
		if ($('#slideshow-pause-play-button').hasClass('play')){
			$('#slideshow-pause-play-button').removeClass('play');
			$('#slideshow-pause-play-button').addClass('pause');
		}
		else {
			$('#slideshow-pause-play-button').removeClass('pause');
			$('#slideshow-pause-play-button').addClass('play');
			if($('#slideshow-shrink-enlarge-button').hasClass('shrink')) {
				var intLeftOver = sliderList.length + (parseInt($('#slideshow-inner-container').css('left'))/Math.max(document.documentElement.clientWidth, window.innerWidth || 0));
			}
			else {
				var intLeftOver = sliderList.length + parseInt($('#slideshow-inner-container').css('left'))/620;
			}
			for(i=intLeftOver;i>1;i--){
					currentQueue.push(setTimeout(autoPlay, i*autoplaySpeed));
			}
		}
		});
	
	$('#slideshow-right-arrow').click(function(){
		if ($('#slideshow-pause-play-button').hasClass('play')){
			$('#slideshow-pause-play-button').removeClass('play');
			$('#slideshow-pause-play-button').addClass('pause');
		}
		for(i=0;i<currentQueue.length-1;i=i+1){
			clearTimeout(currentQueue[i]);
		}
		currentQueue = [];
		if($('#slideshow-shrink-enlarge-button').hasClass('shrink')) {
			var playType = [100,'vw'];
			var currentPos = (parseInt($('#slideshow-inner-container').css('left'))/Math.max(document.documentElement.clientWidth, window.innerWidth || 0))*100;
			if(sliderList.length + (parseInt($('#slideshow-inner-container').css('left'))/Math.max(document.documentElement.clientWidth, window.innerWidth || 0)) > 1){
				var leftOver = true;
			}
			else {
				var leftOver = false;
			}
		}
		else {
			var playType = [620,'px'];
			var currentPos = parseInt($('#slideshow-inner-container').css('left'));
			if(sliderList.length + parseInt($('#slideshow-inner-container').css('left'))/playType[0] > 1) {
				var leftOver = true;
			}
			else {
				var leftOver = false;
			}
		}
		if (leftOver){
			$('#slideshow-inner-container').animate({left:currentPos-playType[0] + playType[1]});
			$('#slideshow-number-current')[0].innerHTML++;
		}
		else {
			$('#slideshow-inner-container').animate({left:0});
			$('#slideshow-number-current')[0].innerHTML = 1;
		}
	});
	
	$('#slideshow-left-arrow').click(function(){
		if ($('#slideshow-pause-play-button').hasClass('play')){
			$('#slideshow-pause-play-button').removeClass('play');
			$('#slideshow-pause-play-button').addClass('pause');
		}
		for(i=0;i<currentQueue.length-1;i=i+1){
			clearTimeout(currentQueue[i]);
		}
		currentQueue = [];
		if($('#slideshow-shrink-enlarge-button').hasClass('shrink')) {
			var playType = [100,'vw'];
			var currentPos = (parseInt($('#slideshow-inner-container').css('left'))/Math.max(document.documentElement.clientWidth, window.innerWidth || 0))*100;
			if(sliderList.length + (parseInt($('#slideshow-inner-container').css('left'))/Math.max(document.documentElement.clientWidth, window.innerWidth || 0)) != sliderList.length){
				var leftOver = true;
			}
			else {
				var leftOver = false;
			}
		}
		else {
			var playType = [620,'px'];
			var currentPos = parseInt($('#slideshow-inner-container').css('left'));
			if(sliderList.length + parseInt($('#slideshow-inner-container').css('left'))/playType[0] != sliderList.length) {
				var leftOver = true;
			}
			else {
				var leftOver = false;
			}
		}
		if (leftOver){
			$('#slideshow-inner-container').animate({left:currentPos+playType[0] + playType[1]});
			$('#slideshow-number-current')[0].innerHTML--;
		}
		else {
			$('#slideshow-inner-container').animate({left:-playType[0]*(sliderList.length-1) + playType[1]});
			$('#slideshow-number-current')[0].innerHTML = sliderList.length;
		}
	});
	
	$('#slideshow-shrink-enlarge-button').click(function(){
		if ($('#slideshow-shrink-enlarge-button').hasClass('enlarge')){
			$('#slideshow-shrink-enlarge-button').removeClass('enlarge');
			$('#slideshow-shrink-enlarge-button').addClass('shrink');
			$('#slideshow-main-container').css({
				position: 'fixed',
				top: 0,
				right: 0,
				bottom: 0,
				left: 0,
				width: '100%',
				height: '100%'
			});
			$('#slideshow-left-arrow').css({
				position: 'absolute',
				left: 0,
				'line-height': '100vh',
				height: '100vh',
				'z-index': 5
			});
			$('#slideshow-left-arrow img').css({
				'vertical-align': 'middle'
			});
			$('.slider img').css({
				position: 'absolute',
				top: '50%',
				left: '50%',
				'-webkit-transform': 'translate(-50%, -50%)',
				'-moz-transform': 'translate(-50%, -50%)',
				'-ms-transform': 'translate(-50%, -50%)',
				'-o-transform': 'translate(-50%, -50%)',
				transform: 'translate(-50%, -50%)',
				width: 'initial',
				height: 'initial',
				'max-width': '100vw',
				'max-height': '100vh',
				'z-index': '-2'
			});
			$('.slider').css({
				position: 'absolute',
				top: 0,
				width: '100vw',
				height: '100vh',
			});
			$('.slider').each(function(index){
				$(this).css({
					left: index * 100 + 'vw'
				});
			});
			$('#slideshow-inner-container').css({
				width: sliderList.length * 100 + 'vw',
				height: '100vh',
				left: ($('#slideshow-number-current')[0].innerHTML-1) * -100 + 'vw'
			});
			$('#slideshow-content-container').css({
				height: '100vh',
				width: '100vw'
			});
			$('#slideshow-right-arrow').css({
				left: 'auto',
				'line-height': '100vh',
				height: '100vh',
				'z-index': 5
			});
			$('#slideshow-right-arrow img').css({
				'vertical-align': 'middle'
			});
			$('#slideshow-controls').css({
				width: '100vw',
				position: 'absolute',
				bottom: 0
			});
			$('#slideshow-shrink-enlarge-button').css({
				right: '65px'
			});
			$('.slideshow-title-overlay').css({
				bottom: '40px',
				'z-index': '-1'
			});
			$('#slideshow-pause-play-button').css({
				left: '40px'
			});
			$('#slideshow-number').css({
				left: '100px'
			});
			$('#slideshow-titles').css({
				left: '220px'
			});
			$('#slideshow-speed').css({
				right: '140px'
			});
			$('#page-wrapper').css({
				overflow: 'hidden'
			});
			$('#slideshow-preview-container').css({
				display: 'none'
			});
		}
		else {
			$('#slideshow-shrink-enlarge-button').removeClass('shrink');
			$('#slideshow-shrink-enlarge-button').addClass('enlarge');
			$('#slideshow-main-container').css({
				position: 'relative',
				top: 'initial',
				right: 'initial',
				bottom: 'initial',
				left: 'initial',
				width: '700px',
				height: '400px'
			});
			$('#slideshow-left-arrow').css({
				position: 'initial',
				left: 'initial',
				'line-height': 'initial',
				height: '360px',
				'z-index': 'initial'
			});
			$('#slideshow-left-arrow img').css({
				'vertical-align': 'initial'
			});
			$('.slider img').css({
				position: 'initial',
				top: 'initial',
				left: 'initial',
				'-webkit-transform': 'initial',
				'-moz-transform': 'initial',
				'-ms-transform': 'initial',
				'-o-transform': 'initial',
				transform: 'initial',
				width: 'initial',
				height: 'initial',
				'max-width': '620px',
				'max-height': '360px',
				'z-index': 'initial'
			});
			$('.slider').css({
				position: 'relative',
				top: 'initial',
				width: '620px',
				height: '360px',
			});
			$('.slider').each(function(index){
				$(this).css({
					left: 0
				});
			});
			$('#slideshow-inner-container').css({
				width: sliderList.length * 620 + 'px',
				height: 'initial',
				left: ($('#slideshow-number-current')[0].innerHTML-1) * -620 + 'px'
			});
			$('#slideshow-content-container').css({
				width: '620px',
				height: '360px'
			});
			$('#slideshow-right-arrow').css({
				left: '660px',
				'line-height': 'initial',
				height: '360px',
				'z-index': 'initial'
			});
			$('#slideshow-right-arrow img').css({
				'vertical-align': 'initial'
			});
			$('#slideshow-controls').css({
				width: '700px',
				position: 'initial',
				bottom: 'initial'
			});
			$('#slideshow-shrink-enlarge-button').css({
				right: '0px'
			});
			$('.slideshow-title-overlay').css({
				bottom: 0,
				'z-index': 'initial'
			});
			$('#slideshow-pause-play-button').css({
				left: '0'
			});
			$('#slideshow-number').css({
				left: '80px'
			});
			$('#slideshow-titles').css({
				left: '200px'
			});
			$('#slideshow-speed').css({
				right: '100px'
			});
			$('#page-wrapper').css({
				overflow: 'visible'
			});
			$('#slideshow-preview-container').css({
				display: 'block'
			});
		}
	});
	
	$('#slideshow-titles').click(function(){
		if($('#slideshow-titles')[0].innerHTML == "Hide title info"){
			$('#slideshow-titles')[0].innerHTML = "Show title info";
			$('.slideshow-title-overlay').addClass('hidden');
		}
		else {
			$('#slideshow-titles')[0].innerHTML = "Hide title info";
			$('.slideshow-title-overlay').removeClass('hidden');
		}
	});
	
	$('#slideshow-preview-left-arrow').click(function(){
		var currentPreviewPos = parseInt($('#slideshow-preview-inner-container').css('left'));
		var currentPreviewWidth = parseInt($('#slideshow-preview-container')[0].scrollWidth);
		if(currentPreviewPos < 0) {
			$('#slideshow-preview-inner-container').animate({left: currentPreviewPos + 195 + 'px'});
		}
	});
	
	$('#slideshow-preview-right-arrow').click(function(){
		var currentPreviewPos = parseInt($('#slideshow-preview-inner-container').css('left'));
		var currentPreviewWidth = parseInt($('#slideshow-preview-inner-container').css('width'));
		if(currentPreviewWidth - 55 - 760 + currentPreviewPos > 195) {
			$('#slideshow-preview-inner-container').animate({left: currentPreviewPos - 195 + 'px'});
		}
	});
});

var toggleFavorites = function(humID) {
	var tempClass = '';
	if ($('#fav-button').hasClass('not-fav')) {
		tempClass = 'temp-fav';
	}
	else {
		tempClass = 'temp-not-fav';
	}
	$.post("http://www.colibricollection.com/favorites?hum-id=" + humID);
	$('#fav-button').toggleClass('not-fav fav');
	$('#fav-button').addClass(tempClass);
	setTimeout(function(){$('#fav-button').removeClass(tempClass);}, 2000);
};

var toggleSortFavorites = function(humID) {
	var tempClass = '';
	if (!isNaN(humID)) {
		if ($('#favid' + humID).hasClass('sort-not-fav')) {
			tempClass = 'temp-sort-fav';
			document.getElementById('favid' + humID).title = 'Remove from favorites?';
		}
		else {
			tempClass = 'temp-sort-not-fav';
			document.getElementById('favid' + humID).title = 'Add to favorites?';
		} 
		$.post("http://www.colibricollection.com/favorites?hum-id=" + humID);
		$('#favid' + humID).toggleClass('sort-not-fav sort-fav');
		$('#favid' + humID).addClass(tempClass);
		setTimeout(function(){$('#favid' + humID).removeClass(tempClass);}, 2000);
	}
};

var toggleSpeciesOverlay = function(humID) {
	$('#species-whole-overlay').toggleClass('species-whole-overlay hidden');
	$('#' + humID).toggleClass('species-pictures-large-container hidden');
	currentHumID = humID;
};

var toggleReferences = function() {
	$('#species-reference-container').toggleClass('hidden shown');
	if ($('#species-references-button').text() == "show") {
		$('#species-references-button').text("hide");
	}
	else {
		$('#species-references-button').text("show");
	}
};

var toggleThumbnails = function() {
	$('.thumb').toggleClass('sort-hum-thumbnail hidden');
	if ($('#sort-thumbnail-button').text() == "Hide thumbnails") {
		$('#sort-thumbnail-button').text("Show thumbnails");
	}
	else {
		$('#sort-thumbnail-button').text("Hide thumbnails");
	}
};

var calibrateScale = function(scaleMethod, scaleSize) {
	var scaleWidth = $(scaleMethod).width();
	var widthRatio = scaleWidth/scaleSize;
	document.cookie = "scaleRatio=" + widthRatio + "; expires=315360000;path=/";
    $('#calibrate-test-img').css('width', 548 * widthRatio);
	$('#calibrate-status').text('Your screen is currently calibrated.');
	$('#calibrate-success').text('Image resized, calibration complete!');
};

var clearChecklist = function() {
	if(confirm("Are you sure you want to clear the entire checklist?")) {
		$.post("http://www.colibricollection.com/checklist?clear-checklist=True", function(response) {
			if (response == "Success") {
				location.reload(true);
			}
			else {
				alert("Error clearing checklist. Please try again.");
			}
		});
	}
	else {
		return;
	}
};

var clearFavorites = function() {
	if(confirm("Are you sure you want to clear all favorites?")) {
		$.post("http://www.colibricollection.com/favorites?clear-favorites=True", function(response) {
			if (response == "Success") {
				location.reload(true);
			}
			else {
				alert("Error clearing favorites. Please try again.");
			}
		});
	}
	else {
		return;
	}
};

var toggleMainFavorites = function(humID) {
	var parentContainer = $('#favid' + humID).parents().eq(2);
	parentContainer.find('.thumb').toggleClass('favorites-hide-thumbnail');
	parentContainer.find('.sort-hum-name').toggleClass('favorites-hide-name');
	parentContainer.find('.favorites-undo-link').toggleClass('hidden');
	parentContainer.find('.favorites-icons').toggleClass('hidden');
	$.post("http://www.colibricollection.com/favorites?hum-id=" + humID);
};
var gameIndex = 0;
var win = false;
var nextGamePicture = function() {
	if (win){
		gameIndex++;
		if (gameIndex == 342){
			$('#game-results')[0].innerHTML = "Congratulations, you matched all 342 hummingbirds! You can officially call yourself a hummingbird identification expert, and your highscore has been updated.<br><br>If you would like to play again on a harder level, you can change the difficulty in the dropdown.";
			$.post("http://www.colibricollection.com/name-match?level=" + currentLevel + "&highscore=" + $('#match-streak')[0].innerHTML);
			return
		}
		else {
			$('#game-picture').attr('src', gameList[gameIndex]['link']);
			$('#game-picture').attr('name', gameList[gameIndex]['name']);
			$('#answer1').attr('onclick', "javascript:chooseAnswer('#answer-result1', " + '"' + gameList[gameIndex]['optionA'] + '");');
			$('#answer2').attr('onclick', "javascript:chooseAnswer('#answer-result2', " + '"' + gameList[gameIndex]['optionB'] + '");');
			$('#answer3').attr('onclick', "javascript:chooseAnswer('#answer-result3', " + '"' + gameList[gameIndex]['optionC'] + '");');
			$('#answer4').attr('onclick', "javascript:chooseAnswer('#answer-result4', " + '"' + gameList[gameIndex]['optionD'] + '");');
			$('#answer1')[0].innerHTML = gameList[gameIndex]['optionA'] + " <span id='answer-result1'></span>";
			$('#answer2')[0].innerHTML = gameList[gameIndex]['optionB'] + " <span id='answer-result2'></span>";
			$('#answer3')[0].innerHTML = gameList[gameIndex]['optionC'] + " <span id='answer-result3'></span>";
			$('#answer4')[0].innerHTML = gameList[gameIndex]['optionD'] + " <span id='answer-result4'></span>";
		}
	}
	else {
		if (currentHighscore < $('#match-streak')[0].innerHTML){
			$.post("http://www.colibricollection.com/name-match?level=" + currentLevel + "&highscore=" + $('#match-streak')[0].innerHTML);
			$('#game-results')[0].innerHTML = "You lost your streak at " + $('#match-streak')[0].innerHTML + ", but that's a new highscore!<br><br>Would you like to <a class='main-links' onclick='javascript:window.location.reload(true);'>play again?</a>";
		}
		else {
			$('#game-results')[0].innerHTML = "Sorry, you lost your streak at " + $('#match-streak')[0].innerHTML + "." + "Would you like to <a class='main-links' onclick='javascript:window.location.reload(true);'>play again?</a>";
		}
	}
}

var chooseAnswer = function(answerContainer, answer) {
	var answerContainerList = [$('#answer-result1'),
								$('#answer-result2'),
								$('#answer-result3'),
								$('#answer-result4')];
	for (i = 0; i < answerContainerList.length; i++) {
		if (answerContainerList[i].attr('class') == 'correct-answer' || answerContainerList[i].attr('class') == 'wrong-answer') {
		return
		}
	}
	if (answer == $('#game-picture').attr('name')) {
		$(answerContainer).text('correct!');
		$(answerContainer).addClass('correct-answer');
		$('#match-streak')[0].innerHTML++;
		win = true;
	}
	else {
		$(answerContainer).text('wrong!');
		$(answerContainer).addClass('wrong-answer');
		win = false;
		for (i = 1; i < 5; i++){
			if ($('#answer' + i)[0].innerHTML.substring(0,$('#answer' + i)[0].innerHTML.search("<")-1) == $('#game-picture').attr('name')){
			$('#answer-result' + i).addClass('correct-answer');
			$('#answer-result' + i).text('this was correct');
			}
		}
	}
	setTimeout(nextGamePicture, 1000);
};

var getCookie = function(name) {
	var cookieName = name + "=";
	var cookieList = document.cookie.split(';');
	for (var i = 0; i < cookieList.length; i++) {
		var cookie = cookieList[i];
		while (cookie.charAt(0) == ' ') {
			cookie = cookie.substring(1);
		}
		if (cookie.indexOf(cookieName) === 0) {
			return cookie.substring(cookieName.length, cookie.length);
		}
	}
	return "";
};

var autoPlay = function(){
	if($('#slideshow-shrink-enlarge-button').hasClass('shrink')) {
		var playType = [100,'vw'];
		var currentPos = (parseInt($('#slideshow-inner-container').css('left'))/Math.max(document.documentElement.clientWidth, window.innerWidth || 0))*100;
		if(sliderList.length + (parseInt($('#slideshow-inner-container').css('left'))/Math.max(document.documentElement.clientWidth, window.innerWidth || 0)) > 1){
			var leftOver = true;
		}
		else {
			var leftOver = false;
		}
	}
	else {
		var playType = [620,'px'];
		var currentPos = parseInt($('#slideshow-inner-container').css('left'));
		if(sliderList.length + parseInt($('#slideshow-inner-container').css('left'))/playType[0] > 1) {
			var leftOver = true;
		}
		else {
			var leftOver = false;
		}
	}
	if ($('#slideshow-pause-play-button').hasClass('play') && leftOver){
		$('#slideshow-inner-container').animate({left:currentPos-playType[0] + playType[1]});
		$('#slideshow-number-current')[0].innerHTML++;
	}
};
var currentQueue = [];