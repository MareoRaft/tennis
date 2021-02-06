import React from 'react'

import * as am4core from '@amcharts/amcharts4/core'
import * as am4charts from '@amcharts/amcharts4/charts'
import am4themes_animated from '@amcharts/amcharts4/themes/animated'

// See for chart usage:
// https://www.amcharts.com/docs/v4/getting-started/integrations/using-react/

// Set theme
am4core.useTheme(am4themes_animated)


const getRandomData = () => {
	const data = []
	let value = 50
	for (let i = 0; i < 300; i++) {
		let date = new Date()
		date.setHours(0, 0, 0, 0)
		date.setDate(i)
		value -= Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 10)
		data.push({date, value})
	}
	return data
}


class Chart extends React.Component {
	componentDidMount() {
		const chart = am4core.create('chartdiv', am4charts.XYChart)
		chart.data = getRandomData()

		let dateAxis = chart.xAxes.push(new am4charts.DateAxis())
		dateAxis.renderer.minGridDistance = 60

		chart.yAxes.push(new am4charts.ValueAxis())

		let series = chart.series.push(new am4charts.LineSeries())
		series.dataFields.valueY = 'value'
		series.dataFields.dateX = 'date'
		series.tooltipText = '{value}'
		series.tooltip.pointerOrientation = 'vertical'

		chart.cursor = new am4charts.XYCursor()
		chart.cursor.snapToSeries = series
		chart.cursor.xAxis = dateAxis

		chart.scrollbarX = new am4core.Scrollbar()

		this.chart = chart
	}
	componentDidUpdate(oldProps) {
		if (this.props.updateNum !== oldProps.updateNum) {
			this.chart.data = getRandomData()
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
				style={{width: '100%', height: '500px'}}
				onClick={this.props.onClick}
			>
			</div>
		);
	}
}

export default Chart;
