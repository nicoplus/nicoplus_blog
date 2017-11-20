// Dropzone.options.idPostBanner = {
// 	autoProcessQueue:false,
// 	addRemoveLinks: true,
// 	paramName: 'banner-image',
// 	init: function() {
// 		var that = this
// 		$('#id-button-submit').bind('click', function(event){
// 			that.processQueue()
// 		})
// 	}
// }

var loadDropzone = function() {
	Dropzone.autoDiscover = false;
	var idPostBanner = new Dropzone("#id-post-banner", {
	    url: "/api/post/upload/image",
	    addRemoveLinks: true,
	    method: 'post',
	    acceptedFiles: 'image/*',
	    dictRemoveFile: '取消上传',
	    maxFiles: 1,
	});

	idPostBanner.on('success', function(file, response){
		var imageUrlInput = qs('#image_id')
		imageUrlInput.value = response.id
		file.uploaded = true
	})

	idPostBanner.on('removedfile', function(file) {
		if (file.uploaded == true) {
			deleteImageBanner()
		}
		
	})

	idPostBanner.on('maxfilesexceeded',function(file){
	    idPostBanner.removeFile(file)
	})
}

var deleteImageBanner = function() {
	var imageIdInput = qs('#image_id')
	var imageId = imageIdInput.value
	if (imageId != '') {
		$.ajax({
			type: 'GET',
			url: `/api/post/delete/image?id=${imageId}`,
			success: function(response) {
				log(response)
				imageIdInput.value = ""
			}
		})
	}
}

var getArticle = function(id){
	var data = {
		title: '',
		body: '',
	}
	if (window.location.search != '') {
		$.ajax({
			type:'GET',
			url:`/api/get/post?id=${id}`,
			success:function(response){
				log(response);
				var r = JSON.parse(response)
				data.title = r.title
				data.body = r.body
			},
		});
	}
	loadVue(data)

}



var loadVue = function(data) {
	var formVue = new Vue({
		el: '#id-post-form',
		data: {
			title: 'hello',
			body: '# hello',
		},
		methods: {
			submit: function(){
				log('submit')
				var title = this.$refs.title
				var body = this.$refs.body
				var imageId = this.$refs.imageId
				var csrfToken = qs('#csrf_token')
				log('title', title.value)
				log('body', body.value)
				log('imageId', imageId.value)
				log('csrfToken', csrfToken.value)
				if (title.checkValidity() && body.checkValidity()) {
					axios.post('/api/post/upload/post', {
					    title: title.value,
					    body: body.value,
					    image_id: 'imageId.value',
					    csrf_token: csrfToken.value,
					  	},
					  	{headers: {
	      					'X-CSRFToken': csrfToken.value,
	    					},
	    				}
	
	    			)
					  .then(function (response) {
					    console.log('response',response);
					  })
					  .catch(function (error) {
					    console.log(error);
					  });
				}
			}
		},
	})
}

var loadArticleContent = function() {
	getArticle()
}

var loadPostEdit = function(){
	loadDropzone()
	loadArticleContent()
}


$( document ).ready(function(){
	loadPostEdit()
})