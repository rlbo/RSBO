from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
import sys
import os
import os.path
import numpy as np
import pickle
from pickle import dump
import scipy.io
import matplotlib as mpl
import matplotlib.pyplot as plt


def opt(a, b):
	if prob_name in ['it10']:
		return max(a, b)
	else:
		return min(a, b)

def load_maml(_dir, prob_name, reps):
	folder = 'results_' + prob_name + '/'
	cum_costs = []
	values = []
	opt_values = []

	for seed in range(reps):
		with open(folder + '{}_results.pickle'.format(seed), 'rb') as file: 
			f_dict = pickle.load(file)

		costs = f_dict.get('train_costs_sum')
		cum_costs.append(np.cumsum(costs))

		if prob_name in ['it10']:
			value = f_dict.get('test_returns_mean')
		else:
			value = f_dict.get('test_costs_mean')
		values.append(value)

		opt_value = [value[0]]
		for v in value[1:]:
			opt_value.append(opt(opt_value[-1], v))
		opt_values.append(opt_value)

		# with open(folder + '{}_results_1.pickle'.format(seed), "wb") as file: 
		# 	dump(f_dict, file, protocol=2)

	return np.array(cum_costs), np.array(values), np.array(opt_values)


def plot(prob_name, _dir, reps):

	new_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
			  '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
			  '#bcbd22', '#17becf']

	colors = {
		'besd': new_colors[3], 
		'EI': new_colors[1], 
		'LCB': new_colors[4], 
		'hb': new_colors[2],
		'transferQL': new_colors[0],
		'maml': new_colors[5]
		}
	labels = {
		'besd': r'BESD', 
		'EI': r'EI', 
		'LCB': r'LCB', 
		'hb': r'HB',
		'transferQL': r'transferQL',
		'maml': r'maml',
		}
	alpha = {
		'besd': 0.9, 
		'EI': 0.9, 
		'LCB': 0.6, 
		'hb': 0.8,
		'transferQL': 0.6,
		'maml': 0.8,
		}
	markersize = 4
	linewidth = 2
	barwidth = 0.75
	label_size = 15
	legend_size = 12
	tick_size = 12

	# -------------- error bar with cost -------------- #
	cum_costs, values, opt_values = load_maml(_dir, prob_name, reps)
	plot_values = values

	step = 2e5
	if prob_name == 'gw10Two1': step, loc = 2e5, 'center right'
	elif prob_name == 'gw20Three1': step, loc = 1e6, 'upper right'
	elif prob_name == 'ky': step, loc = 2e5, 'lower left'
	elif prob_name == 'it10': step, loc = 5e5, 'lower right'
	elif prob_name=='mc': step, loc = 2e6, 'upper right'

	x_lim = np.mean(cum_costs, axis=0)[-1]
	num_pts = 50

	mpl.rcParams['font.family'] = 'serif' # monospace
	mpl.rcParams['font.weight'] = 100

	fig, ax = plt.subplots(figsize=(5,3))
	plt.xlabel('Total cost', fontsize=label_size)
	if prob_name in ['it10']:
		plt.ylabel('Reward', fontsize=label_size)
	else:
		plt.ylabel('Steps', fontsize=label_size)

	alg = 'maml'

	markers, caps, bars = ax.errorbar(np.mean(cum_costs, axis=0), 
									  np.mean(plot_values, axis=0),
									  yerr=plot_values.std(axis=0) / np.sqrt(num_pts) * 2.0, 
									  color=colors[alg], alpha=1, label=labels[alg], 
									  elinewidth=barwidth, linestyle='-', linewidth=linewidth)
	# print(alg, np.vstack((np.mean(Cum_cost[alg][:num_pts], axis=0), np.mean(Opt_value[alg][:num_pts], axis=0))).T)
	[cap.set_alpha(0.5) for cap in caps]

	plt.grid(True)
	if prob_name=='ky10One': plt.ylim([130, 480])
	plt.xlim([0, x_lim])
	plt.xticks(np.arange(0, x_lim, step=step), fontsize=tick_size)
	plt.yticks(fontsize=tick_size)
	plt.ticklabel_format(axis='x', style='sci', scilimits=(5,6), useMathText=True)
	plt.legend(loc=loc, fontsize=legend_size, ncol=2)
	plt.tight_layout()
	plt.savefig(_dir + 'errorbar_cost_' + prob_name + '.pdf')
	plt.close()


if __name__ == '__main__':
	argv = sys.argv[1:]
	'''
	python results_processing.py ky
		gw10Two1
		gw20Three1
		ky
		it10
	'''
	prob_name = argv[0]

	_dir = 'results_plots/'
	if not os.path.exists(_dir):
		os.makedirs(_dir)

	plot(prob_name, _dir, 20)
