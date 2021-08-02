import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import tilemapbase
import pandas as pd


def draw_sensor_network_with_traffic(sensor_location_csv_path='data/graph_sensor_locations_bay.csv',
                                     traffic_csv_path='data/12.csv', tag='truth',
                                     save_fig_prefix='fig'):
    df_meta = pd.read_csv(sensor_location_csv_path, index_col=0, names=['latitude', 'longitude'])
    df_speed = pd.read_csv(traffic_csv_path, index_col=0)

    tilemapbase.init(create=True)

    # The path to plot
    longs = df_meta['longitude'].values
    lats = df_meta['latitude'].values

    # extent
    degree_range = 0.05
    extent = tilemapbase.Extent.from_lonlat(df_meta['longitude'].min() - degree_range,
                                            df_meta['longitude'].max() + degree_range,
                                            df_meta['latitude'].min() - degree_range,
                                            df_meta['latitude'].max() + degree_range)
    extent = extent.to_aspect(1.3)
    plotter = tilemapbase.Plotter(extent, tilemapbase.tiles.Stamen_Terrain, width=400)
    # Convert to web mercator
    path = [tilemapbase.project(x, y) for x, y in zip(longs, lats)]
    x, y = zip(*path)

    fig, ax = plt.subplots(figsize=(5, 5), dpi=600)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    plotter.plot(ax, alpha=0.8)
    scat = ax.scatter(x, y, c=df_speed.loc[df_meta.index][tag].values, vmin=20, vmax=70, cmap='RdYlGn')

    # create an axes on the right side of ax. The width of cax will be 5%
    # of ax and the padding between cax and ax will be fixed at 0.05 inch.
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad=0.05)

    plt.colorbar(scat, cax=cax)
    plt.savefig(f'data/{save_fig_prefix}_{tag}.pdf', bbox_inches='tight')


if __name__ == '__main__':
    horizons = [3, 6, 12]
    for h in horizons:
        traffic_csv_path = f'data/{h}.csv'
        save_fig_prefix = f'fig_{h}'
        draw_sensor_network_with_traffic(tag='truth', traffic_csv_path=traffic_csv_path, save_fig_prefix=save_fig_prefix)
        draw_sensor_network_with_traffic(tag='prediction', traffic_csv_path=traffic_csv_path, save_fig_prefix=save_fig_prefix)
