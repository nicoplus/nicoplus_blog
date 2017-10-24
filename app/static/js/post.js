Dropzone.options.idPostBanner = {
	autoProcessQueue:false,
	addRemoveLinks: true,
	paramName: 'banner-image',
	init: function() {
		var that = this
		$('#id-button-submit').bind('click', function(event){
			that.processQueue()
		})
	}
}

var app6 = new Vue({
	el: '#app-6',
	data:{
		content:'# Hello',
		title:'hao'
	},
	computed:{
		marked_m:function(){
			return marked(this.content)
		}
	},
	methods: {
		submit:function(){
			content = this.content
			title = this.title
			console.log('title',title)
			axios.post('/api/post/upload/post', {
			    title: title,
			    content: content,
			  })
			  .then(function (response) {
			    console.log(response);
			  })
			  .catch(function (error) {
			    console.log(error);
			  })
			
		}
	}	
})