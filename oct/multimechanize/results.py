#!/usr/bin/env python
#
#  Copyright (c) 2010-2012 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3
#
#  This file is part of Multi-Mechanize | Performance Test Framework
#


import time
import json
from collections import defaultdict
from . import graph
from . import reportwriter
from . import reportwriterxml
from oct.results.reportresults import Results, ReportResults


def output_results(results_dir, results_file, run_time, rampup, ts_interval, user_group_configs=None,
                   xml_reports=False, parent='../../'):
    results = Results(results_dir + results_file, run_time)

    report = reportwriter.Report(results_dir, parent)

    print('transactions: %i' % results.total_transactions)
    print('errors: %i' % results.total_errors)
    print('')
    print('test start: %s' % results.start_datetime)
    print('test finish: %s' % results.finish_datetime)
    print('')



    # report.write_line('<h1>Performance Results Report</h1>')

    # report.write_line('<h2>Summary</h2>')

    # report.write_line('<div class="summary">')
    # report.write_line('<b>transactions:</b> %d<br />' % results.total_transactions)
    # report.write_line('<b>errors:</b> %d<br />' % results.total_errors)
    # report.write_line('<b>run time:</b> %d secs<br />' % run_time)
    # report.write_line('<b>rampup:</b> %d secs<br /><br />' % rampup)
    # report.write_line('<b>test start:</b> %s<br />' % results.start_datetime)
    # report.write_line('<b>test finish:</b> %s<br /><br />' % results.finish_datetime)
    # report.write_line('<b>time-series interval:</b> %s secs<br /><br /><br />' % ts_interval)
    # if user_group_configs:
    #     report.write_line('<b>workload configuration:</b><br /><br />')
    #     report.write_line('<table>')
    #     report.write_line('<tr><th>group name</th><th>threads</th><th>script name</th></tr>')
    #     for user_group_config in user_group_configs:
    #         report.write_line('<tr><td>%s</td><td>%d</td><td>%s</td></tr>' %
    #                           (user_group_config.name, user_group_config.num_threads, user_group_config.script_file))
    #     report.write_line('</table>')
    # report.write_line('</div>')

    # report.write_line('<h2>All Transactions</h2>')

    report_results = ReportResults(results, ts_interval)
    report_results.set_all_transactions_results()
    report_results.set_custom_timers()

    graph.resp_graph_raw(report_results.all_results['trans_timer_points'], 'All_Transactions_response_times.svg', results_dir)
    graph.resp_graph(report_results.all_results['interval_results'].avg_resptime_points,
                     report_results.all_results['interval_results'].percentile_80,
                     report_results.all_results['interval_results'].percentile_90,
                     'All_Transactions_response_times_intervals.svg', results_dir)


    # # all transactions - response times
    # trans_timer_points = []  # (elapsed, timervalue)
    # trans_timer_vals = []
    # for resp_stats in results.resp_stats_list:
    #     t = (resp_stats.elapsed_time, resp_stats.trans_time)
    #     trans_timer_points.append(t)
    #     trans_timer_vals.append(resp_stats.trans_time)
    # graph.resp_graph_raw(trans_timer_points, 'All_Transactions_response_times.svg', results_dir)

    # report.write_line('<h3>Transaction Response Summary (secs)</h3>')
    # report.write_line('<table>')
    # report.write_line('<tr><th>count</th><th>min</th><th>avg</th><th>80pct</th>'
    #                   '<th>90pct</th><th>95pct</th><th>max</th><th>stdev</th></tr>')
    # report.write_line('<tr><td>%i</td><td>%.3f</td><td>%.3f</td><td>%.3f</td>'
    #                   '<td>%.3f</td><td>%.3f</td><td>%.3f</td><td>%.3f</td></tr>' % (results.total_transactions,
    #                                                                                  min(trans_timer_vals),
    #                                                                                  average(trans_timer_vals),
    #                                                                                  percentile(trans_timer_vals, 80),
    #                                                                                  percentile(trans_timer_vals, 90),
    #                                                                                  percentile(trans_timer_vals, 95),
    #                                                                                  max(trans_timer_vals),
    #                                                                                  standard_dev(trans_timer_vals),))
    # report.write_line('</table>')

    # # all transactions - interval details
    # avg_resptime_points = {}  # {intervalnumber: avg_resptime}
    # percentile_80_resptime_points = {}  # {intervalnumber: 80pct_resptime}
    # percentile_90_resptime_points = {}  # {intervalnumber: 90pct_resptime}
    # interval_secs = ts_interval
    # splat_series = split_series(trans_timer_points, interval_secs)
    # report.write_line('<h3>Interval Details (secs)</h3>')
    # report.write_line('<table>')
    # report.write_line('<tr><th>interval</th><th>count</th><th>rate</th><th>min</th><th>avg</th>'
    #                   '<th>80pct</th><th>90pct</th><th>95pct</th><th>max</th><th>stdev</th></tr>')
    # for i, bucket in enumerate(splat_series):
    #     interval_start = int((i + 1) * interval_secs)
    #     cnt = len(bucket)

    #     if cnt == 0:
    #         report.write_line('<tr><td>%i</td><td>0</td><td>0</td><td>N/A</td><td>N/A</td>'
    #                           '<td>N/A</td><td>N/A</td><td>N/A</td><td>N/A</td><td>N/A</td></tr>' % (i + 1))
    #     else:
    #         rate = cnt / float(interval_secs)
    #         mn = min(bucket)
    #         avg = average(bucket)
    #         pct_80 = percentile(bucket, 80)
    #         pct_90 = percentile(bucket, 90)
    #         pct_95 = percentile(bucket, 95)
    #         mx = max(bucket)
    #         stdev = standard_dev(bucket)
    #         report.write_line('<tr><td>%i</td><td>%i</td><td>%.2f</td><td>%.3f</td><td>%.3f</td>'
    #                           '<td>%.3f</td>'
    #                           '<td>%.3f</td><td>%.3f</td><td>%.3f</td><td>%.3f</td></tr>' % (i + 1,
    #                                                                                          cnt,
    #                                                                                          rate,
    #                                                                                          mn,
    #                                                                                          avg,
    #                                                                                          pct_80,
    #                                                                                          pct_90, pct_95,
    #                                                                                          mx,
    #                                                                                          stdev))

    #         avg_resptime_points[interval_start] = avg
    #         percentile_80_resptime_points[interval_start] = pct_80
    #         percentile_90_resptime_points[interval_start] = pct_90

    # report.write_line('</table>')
    # graph.resp_graph(avg_resptime_points, percentile_80_resptime_points, percentile_90_resptime_points,
    #                  'All_Transactions_response_times_intervals.svg', results_dir)

    # report.write_line('<h3>Graphs</h3>')
    # report.write_line('<h4>Response Time: %s sec time-series</h4>' % ts_interval)
    # report.write_line('<figure><embed ype="image/svg+xml" src="All_Transactions_response_times_intervals.svg" />'
    #                   '</figure>')
    # report.write_line('<h4>Response Time: raw data (all points)</h4>')
    # report.write_line('<figure><embed ype="image/svg+xml" src="All_Transactions_response_times.svg" /></figure>')
    # report.write_line('<h4>Throughput: 5 sec time-series</h4>')
    # report.write_line('<figure><embed ype="image/svg+xml" src="All_Transactions_throughput.svg" /></figure>')

    # # all transactions - throughput
    # throughput_points = {}  # {intervalnumber: numberofrequests}
    # interval_secs = ts_interval
    # splat_series = split_series(trans_timer_points, interval_secs)
    # for i, bucket in enumerate(splat_series):
    #     throughput_points[int((i + 1) * interval_secs)] = (len(bucket) / interval_secs)
    # graph.tp_graph(throughput_points, 'All_Transactions_throughput.svg', results_dir)

    # # custom timers
    # for timer_name in sorted(results.uniq_timer_names):
    #     custom_timer_vals = []
    #     custom_timer_points = []
    #     for resp_stats in results.resp_stats_list:
    #         try:
    #             val = resp_stats.custom_timers[timer_name]
    #             custom_timer_points.append((resp_stats.elapsed_time, val))
    #             custom_timer_vals.append(val)
    #         except KeyError:
    #             pass
    #     graph.resp_graph_raw(custom_timer_points, timer_name + '_response_times.svg', results_dir)

    #     throughput_points = {}  # {intervalnumber: numberofrequests}
    #     interval_secs = ts_interval
    #     splat_series = split_series(custom_timer_points, interval_secs)
    #     for i, bucket in enumerate(splat_series):
    #         throughput_points[int((i + 1) * interval_secs)] = (len(bucket) / interval_secs)
    #     graph.tp_graph(throughput_points, timer_name + '_throughput.svg', results_dir)

    #     report.write_line('<hr />')
    #     report.write_line('<h2>Custom Timer: %s</h2>' % timer_name)

    #     report.write_line('<h3>Timer Summary (secs)</h3>')

    #     report.write_line('<table>')
    #     report.write_line('<tr><th>count</th><th>min</th><th>avg</th><th>80pct</th>'
    #                       '<th>90pct</th><th>95pct</th><th>max</th><th>stdev</th></tr>')
    #     report.write_line('<tr><td>%i</td><td>%.3f</td><td>%.3f</td><td>%.3f</td>'
    #                       '<td>%.3f</td><td>%.3f</td><td>%.3f</td><td>%.3f</td>'
    #                       '</tr>' % (len(custom_timer_vals),
    #                                  min(custom_timer_vals),
    #                                  average(custom_timer_vals),
    #                                  percentile(custom_timer_vals, 80),
    #                                  percentile(custom_timer_vals, 90),
    #                                  percentile(custom_timer_vals, 95),
    #                                  max(custom_timer_vals),
    #                                  standard_dev(custom_timer_vals)))
    #     report.write_line('</table>')

    #     # custom timers - interval details
    #     avg_resptime_points = {}  # {intervalnumber: avg_resptime}
    #     percentile_80_resptime_points = {}  # {intervalnumber: 80pct_resptime}
    #     percentile_90_resptime_points = {}  # {intervalnumber: 90pct_resptime}
    #     interval_secs = ts_interval
    #     splat_series = split_series(custom_timer_points, interval_secs)
    #     report.write_line('<h3>Interval Details (secs)</h3>')
    #     report.write_line('<table>')
    #     report.write_line('<tr><th>interval</th><th>count</th><th>rate</th><th>min</th>'
    #                       '<th>avg</th><th>80pct</th><th>90pct</th><th>95pct</th><th>max</th><th>stdev</th></tr>')
    #     for i, bucket in enumerate(splat_series):
    #         interval_start = int((i + 1) * interval_secs)
    #         cnt = len(bucket)

    #         if cnt == 0:
    #             report.write_line('<tr><td>%i</td><td>0</td><td>0</td><td>N/A</td><td>N/A</td>'
    #                               '<td>N/A</td><td>N/A</td><td>N/A</td><td>N/A</td><td>N/A</td></tr>' % (i + 1))
    #         else:
    #             rate = cnt / float(interval_secs)
    #             mn = min(bucket)
    #             avg = average(bucket)
    #             pct_80 = percentile(bucket, 80)
    #             pct_90 = percentile(bucket, 90)
    #             pct_95 = percentile(bucket, 95)
    #             mx = max(bucket)
    #             stdev = standard_dev(bucket)

    #             report.write_line('<tr><td>%i</td><td>%i</td><td>%.2f</td><td>%.3f</td>'
    #                               '<td>%.3f</td><td>%.3f</td><td>%.3f</td><td>%.3f</td><td>%.3f</td>'
    #                               '<td>%.3f</td></tr>' % (i + 1, cnt, rate, mn, avg, pct_80, pct_90, pct_95, mx, stdev))

    #             avg_resptime_points[interval_start] = avg
    #             percentile_80_resptime_points[interval_start] = pct_80
    #             percentile_90_resptime_points[interval_start] = pct_90
    #     report.write_line('</table>')
    #     graph.resp_graph(avg_resptime_points, percentile_80_resptime_points,
    #                      percentile_90_resptime_points, timer_name + '_response_times_intervals.svg', results_dir)

    #     report.write_line('<h3>Graphs</h3>')
    #     report.write_line('<h4>Response Time: %s sec time-series</h4>' % ts_interval)
    #     report.write_line('<figure><embed ype="image/svg+xml" src="%s_response_times_intervals.svg" />'
    #                       '</figure>' % timer_name)
    #     report.write_line('<h4>Response Time: raw data (all points)</h4>')
    #     report.write_line('<figure><embed ype="image/svg+xml" src="%s_response_times.svg" /></figure>' % timer_name)
    #     report.write_line('<h4>Throughput: %s sec time-series</h4>' % ts_interval)
    #     report.write_line('<figure><embed ype="image/svg+xml" src="%s_throughput.svg" /></figure>' % timer_name)

    # report.write_line('<hr />')
    # report.write_closing_html()


# def split_series(points, interval):
#     offset = points[0][0]
#     maxval = int((points[-1][0] - offset) // interval)
#     vals = defaultdict(list)
#     for key, value in points:
#         vals[(key - offset) // interval].append(value)
#     series = [vals[i] for i in range(maxval + 1)]
#     return series


# def average(seq):
#     avg = (float(sum(seq)) / len(seq))
#     return avg


# def standard_dev(seq):
#     avg = average(seq)
#     sdsq = sum([(i - avg) ** 2 for i in seq])
#     try:
#         stdev = (sdsq / (len(seq) - 1)) ** .5
#     except ZeroDivisionError:
#         stdev = 0
#     return stdev


# def percentile(seq, percentile):
#     i = int(len(seq) * (percentile / 100.0))
#     seq.sort()
#     return seq[i]


if __name__ == '__main__':
    output_results('./', 'results.json', 60, 30, 10, parent='../../')
