import React from 'react'
import * as am4core from '@amcharts/amcharts4/core'
import * as am4plugins_forceDirected from '@amcharts/amcharts4/plugins/forceDirected'
import am4themes_animated from '@amcharts/amcharts4/themes/animated'

import data from './data'

// See for chart usage:
// https://www.amcharts.com/docs/v4/getting-started/integrations/using-react/

// Set theme
am4core.useTheme(am4themes_animated)




class ForceDirectedTree extends React.Component {
	componentDidMount() {
		const chart = am4core.create('chartdiv', am4plugins_forceDirected.ForceDirectedTree)

		const series = chart.series.push(new am4plugins_forceDirected.ForceDirectedSeries())
		series.tooltip.pointerOrientation = 'vertical'
		series.dataFields.value = 'value'
		series.dataFields.name = 'name'
		series.dataFields.children = 'children'
		series.nodes.template.tooltipText = '{name}: {value}'
		series.nodes.template.fillOpacity = 0.5
		series.nodes.template.label.text = '{name}'
		series.fontSize = 10
		series.links.template.strokeWidth = 2

		const hoverState = series.links.template.states.create('hover')
		hoverState.properties.strokeWidth = 3
		hoverState.properties.strokeOpacity = 1

		series.nodes.template.events.on("over", function(event) {
		  event.target.dataItem.childLinks.each(function(link) {
		    link.isHover = true;
		  })
		  if (event.target.dataItem.parentLink) {
		    event.target.dataItem.parentLink.isHover = true;
		  }
		})

		series.nodes.template.events.on("out", function(event) {
		  event.target.dataItem.childLinks.each(function(link) {
		    link.isHover = false;
		  })
		  if (event.target.dataItem.parentLink) {
		    event.target.dataItem.parentLink.isHover = false;
		  }
		})

		chart.data = data
		this.chart = chart
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

export default ForceDirectedTree;
