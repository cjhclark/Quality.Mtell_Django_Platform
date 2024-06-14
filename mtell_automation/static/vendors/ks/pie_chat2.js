
var script2=document.getElementById("my_script2");
var pass_rate2=parseFloat(script.getAttribute("pass_rate"));
var fail_rate2=100-pass_rate2
var pass_color2=script2.getAttribute("pass_color");
var fail_color2=script2.getAttribute("fail_color");
var related2=script2.getAttribute("related");
var chart2;
$(document).ready(function() {
	chart2 = new Highcharts.Chart({
		chart2: {
			renderTo: related,
			plotBackgroundColor: null,
			plotBorderWidth: null,
			plotShadow: false
		},
		title: {
			text: '所有表中数据比对通过率(记录维度)'
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