// Loaded via <script> tag, create shortcut to access PDF.js exports.
var pdfjsLib = window['pdfjs-dist/build/pdf'];
// The workerSrc property shall be specified.
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://mozilla.github.io/pdf.js/build/pdf.worker.js';

$("#myPdf").on("change", function(e){
	var file = e.target.files[0]
	if(file.type == "application/pdf"){
		var fileReader = new FileReader();  
		fileReader.onload = function() {
			var pdfData = new Uint8Array(this.result);
			// Using DocumentInitParameters object to load binary data.
			var loadingTask = pdfjsLib.getDocument({data: pdfData});
			loadingTask.promise.then(function(pdf) {
			  console.log('PDF loaded');
			  
			  // Fetch the first page
			  var pageNumber = 1;
			  pdf.getPage(pageNumber).then(function(page) {
				console.log('Page loaded');
				
				var scale = 1.5;
				var viewport = page.getViewport({scale: scale});

				// Prepare canvas using PDF page dimensions
				var canvas = $("#pdfViewer")[0];
				var context = canvas.getContext('2d');
				canvas.height = viewport.height;
				canvas.width = viewport.width;

				// Render PDF page into canvas context
				var renderContext = {
				  canvasContext: context,
				  viewport: viewport
				};
				var renderTask = page.render(renderContext);
				renderTask.promise.then(function () {
				  console.log('Page rendered');
				});
			  });
			}, function (reason) {
			  // PDF loading error
			  console.error(reason);
			});
		};
		fileReader.readAsArrayBuffer(file);
	}
});


// // Show filename, show clear button and change browse 
// //button text when a valid extension file is selected
// $(".browse-button input:file").change(function (){
// 	$("input[name='attachment']").each(function() {
// 	  var fileName = $(this).val().split('/').pop().split('\\').pop();
// 	  $(".filename").val(fileName);
// 	  $(".browse-button-text").html('<i class="fa fa-refresh"></i> Change');
// 	  $(".clear-button").show();
// 	});
//   });
  
//   //actions happening when the button is clicked
//   $('.clear-button').click(function(){
// 	  $('.filename').val("");
// 	  $('.clear-button').hide();
// 	  $('.browse-button input:file').val("");
// 	  $(".browse-button-text").html('<i class="fa fa-folder-open"></i> Browse'); 
//   }); 

function previewFile() {
	  var preview = document.querySelector('audio');
	  var file    = document.querySelector('input[type=file]').files[0];
	  var reader  = new FileReader();
	
	  reader.addEventListener("load", function () {
	    preview.src = reader.result;
	  }, false);
	
	  if (file) {
	    reader.readAsDataURL(file);
	  }
	}