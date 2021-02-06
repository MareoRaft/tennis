import React from 'react'
import * as am4core from '@amcharts/amcharts4/core'
import * as am4charts from '@amcharts/amcharts4/charts'
import am4themes_animated from '@amcharts/amcharts4/themes/animated'
import am4themes_material from '@amcharts/amcharts4/themes/material'
import am4themes_dark from '@amcharts/amcharts4/themes/dark'


// See for chart usage:
// https://www.amcharts.com/docs/v4/getting-started/integrations/using-react/

// Set theme
am4core.useTheme(am4themes_animated)
am4core.useTheme(am4themes_material)
am4core.useTheme(am4themes_dark)


class Component extends React.Component {
	componentDidMount() {
		const chart = am4core.create('chartdiv', am4charts.RadarChart)
		// for initial fade-in
		chart.hiddenState.properties.opacity = 0
		// chart colors can be controlled by list or colorSet
		// chart.colors.list = [
		//   am4core.color("#845EC2"),
		//   am4core.color("#D65DB1"),
		//   am4core.color("#FF6F91"),
		//   am4core.color("#FF9671"),
		//   am4core.color("#FFC75F"),
		//   am4core.color("#F9F871"),
		// ]

		const title = chart.titles.create()
		title.text = 'Top players by statistic chart'
		title.fontSize = 30
		title.marginBottom = 0
		title.align = 'center'
		this.title = title

		const categoryAxis = chart.yAxes.push(new am4charts.CategoryAxis())
		categoryAxis.dataFields.category = 'category'
		categoryAxis.renderer.labels.template.location = 0.5
		categoryAxis.renderer.labels.template.horizontalCenter = 'right'
		categoryAxis.renderer.grid.template.location = 0
		categoryAxis.renderer.grid.template.strokeOpacity = 0.07
		categoryAxis.renderer.axisFills.template.disabled = true
		categoryAxis.interactionsEnabled = false
		categoryAxis.renderer.minGridDistance = 10
		categoryAxis.renderer.inversed = true

		const valueAxis = chart.xAxes.push(new am4charts.ValueAxis())
		valueAxis.tooltip.disabled = true;
		valueAxis.renderer.labels.template.horizontalCenter = "left"
		// https://www.amcharts.com/docs/v4/concepts/axes/value-axis/
		valueAxis.min = 0
		valueAxis.extraMax = 0.2
		valueAxis.renderer.maxLabelPosition = 0.99
		valueAxis.renderer.minGridDistance = 100
		valueAxis.renderer.grid.template.strokeOpacity = 0.07
		valueAxis.renderer.axisFills.template.disabled = true
		valueAxis.interactionsEnabled = false

		const series = chart.series.push(new am4charts.RadarColumnSeries())
		series.columns.template.tooltipText = '{valueX.value}'
		series.name = 'Series 1'
		series.dataFields.categoryY = 'category'
		series.dataFields.valueX = 'value'
		series.stacked = true
		// Make colors change on per-column basis
		series.columns.template.adapter.add('fill', (fill, target) => {
		  return target.dataItem ? chart.colors.getIndex(target.dataItem.index) : fill
		})
		series.columns.template.adapter.add('stroke', (stroke, target) => {
		  return target.dataItem ? chart.colors.getIndex(target.dataItem.index) : stroke
		})

		chart.seriesContainer.zIndex = -1

		chart.cursor = new am4charts.RadarCursor()
		chart.cursor.lineY.disabled = true

		this.chart = chart
	}
	componentDidUpdate(oldProps) {
		if (oldProps.data !== this.props.data) {
			console.log('new data:')
			console.log(this.props.data)
			this.chart.data = this.props.data
			this.title.text = this.props.title
		}
	}
	componentWillUnmount() {
		if (this.chart) {
			this.chart.dispose()
		}
	}
	render() {
		return (
			<div
				id='chartdiv'
				style={{width: '100%', height: '100%'}}
				onClick={this.props.onClick}
			>
			</div>
		);
	}
}

export default Component;
