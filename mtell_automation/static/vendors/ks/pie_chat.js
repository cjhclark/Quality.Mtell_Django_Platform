
var script=document.getElementById("my_script");
var pass_rate=parseFloat(script.getAttribute("pass_rate"));
var fail_rate=parseFloat(script.getAttribute("fail_rate"));
var pass_color=script.getAttribute("pass_color");
var fail_color=script.getAttribute("fail_color");
var related=script.getAttribute("related");
var chart;
$(document).ready(function() {
	chart = new Highcharts.Chart({
		chart: {
			renderTo: related,
			plotBackgroundColor: null,
			plotBorderWidth: null,
			plotShadow: false
		},
		title: {
			text: 'Í¨¹ýÂÊ'
		},
		tooltip: {
			formatter: function() {
				return '<b>'+ this.point.name +'</b>: '+ this.y +' %';
			}
		},
		plotOptions: {
			pie: {
				allowPointSelect: true,
				cursor: 'pointer',
				dataLabels: {
					enabled: true,
					color: '#000000',
					connectorColor: '#000000',
					formatter: function() {
						return '<b>'+ this.point.name +'</b>: '+ this.y +' %';
					}
				}
			}
		},
		series: [{
			type: 'pie',
			name: 'Browser share',
			data: [
				['pass',   pass_rate],
				['fail',   fail_rate],

			]
		}]
	});
});
Highcharts.setOptions({
	colors: [pass_color, fail_color]
});