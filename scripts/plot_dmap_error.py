# coding=utf-8

import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import depth_map_utilities as dmu
import glob

def utf8(data):
	return unicode(data, 'utf-8')

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('sequence_name', help='dataset sequence name')
	parser.add_argument('--diff_list', help='string - name of diff_list file')
	parser.add_argument('--graph_depths', help='directory - graph files')
	args = parser.parse_args()

	sequence_name = args.sequence_name

	limit = int(dmu.MAXDIFF_FIRST_GRAPH / dmu.STEP_FIRST_GRAPH)
	domain = map(lambda x: x * dmu.STEP_FIRST_GRAPH, range(0, limit))

	diff_list_file = "depth_info/diff_list.npy"
	if args.diff_list:
		diff_list_file = args.diff_list

	if not(os.path.isfile(diff_list_file)):
		print "Error: file not found: ", diff_list_file
		return

	print "Using diff list file ", diff_list_file

	# read from npy
	diff_list = np.load(diff_list_file)

	# Discard 0 values at the end
	diff_list_max = 0
	for i in range(0, len(diff_list)):
		if diff_list[i] > 0:
			diff_list_max = i + 1
	diff_list = diff_list[0:diff_list_max]

	major_ticks = np.arange(0, float(diff_list_max) * dmu.STEP_FIRST_GRAPH, 1)
	minor_ticks = np.arange(0, float(diff_list_max) * dmu.STEP_FIRST_GRAPH, dmu.STEP_FIRST_GRAPH)

	fig, ax = plt.subplots()

	index = np.arange(len(diff_list))
	bar_width = 0.10
	opacity = 0.7

	title_font = {
		'fontname':'Ubuntu', 'size':'18', 'color':'black', 'weight':'normal',
		'verticalalignment':'bottom'
	}
	axis_font = {'fontname':'Ubuntu', 'size':'18'}

	rects1 = ax.bar(index * dmu.STEP_FIRST_GRAPH, diff_list, width=bar_width,
					 align='edge', log=True,
	                 alpha=opacity, color='b', edgecolor='b')

	plt.xlabel('Error (metros)', **axis_font)
	plt.ylabel(utf8('Cantidad de píxeles'), **axis_font)
	plt.title(utf8('Error - mapas de profundidad (dense vs. GT) para ' + sequence_name),
			  **title_font)

	ax.set_frame_on(False)
	plt.tick_params(axis='both', which='major', labelsize=15)

	ax.set_xticks(major_ticks)
	ax.set_xticks(minor_ticks, minor=True)
	ax.set_yticks([], minor=True)

	plt.legend()

	ax.grid(which='both')
	ax.grid(which='minor', alpha=0.7)
	ax.grid(which='major', alpha=1, linewidth=2)

	plt.tight_layout()
	plt.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9)


	plt.savefig(sequence_name+"1.png")

	# depth vs errors (amount, mean)
	# load all graph_depth*.npy files

	graph_depth_dir = "./depth_info/"
	if args.graph_depths:
		graph_depth_dir = args.graph_depths

	print "Using graph depth dir: ", graph_depth_dir
	npys = glob.glob(graph_depth_dir+'graph_depth*.npy')

	if len(npys)<=0 :
		print "No data to collect.."
		return
		
	a = np.load(npys[0])
	bins = a[0]
	graph_depth = [[] for i in range(len(bins))]

	for npy in npys:
		actual_graph = np.load(npy)[1]
		for i in range(len(bins)):
			graph_depth[i].extend(actual_graph[i])

	fig = plt.figure(2)
	ax = fig.add_subplot(111)
	bp = ax.boxplot(graph_depth)

	plt.xlabel("Distance to the camera (depth, m)")
	plt.ylabel("Error (m)")
	plt.savefig(sequence_name+"2.png")

	# mean
	plt.figure(3)
	plt.plot(bins, map(lambda x: np.mean(x) if len(x)>0 else 0, graph_depth))
	plt.xlabel("Distance to the camera (depth, m)")
	plt.ylabel("Mean error (m)")
	plt.savefig(sequence_name+"3.png")

	plt.figure(4)
	plt.plot(bins, map(lambda x: np.median(x) if len(x)>0 else 0, graph_depth))
	plt.xlabel("Distance to the camera (depth, m)")
	plt.ylabel("Median error (m)")
	plt.savefig(sequence_name+"4.png")

	plt.figure(5)
	plt.plot(bins, map(lambda x: np.max(x) if len(x)>0 else 0, graph_depth))
	plt.xlabel("Distance to the camera (depth, m)")
	plt.ylabel("Max error (m)")
	plt.savefig(sequence_name+"5.png")


if __name__ == "__main__":
	main()
