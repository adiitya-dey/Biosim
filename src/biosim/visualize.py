import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

class Visualize:

    def visualise(self):
        # Create image directory if it does not exists
        if os.path.isdir(self.img_dir) == False:
            os.mkdir(self.img_dir)
        path = self.img_dir

        # If vis_years = 0 then disable graphics.
        if self.vis_years != 0:
            if year % self.img_years == 0 and year >= self.img_years:
                # Create plot file name
                plotfilename = '{}_{num:05d}.png'.format(self.img_base, num=year)
                plotfilename = os.path.join(path, plotfilename)

                rgb_value = {'W': (0.0, 0.0, 1.0),
                             'L': (0.0, 0.6, 0.0),
                             'H': (0.5, 1.0, 0.5),
                             'D': (1.0, 1.0, 0.5)}
                map_rgb = [[rgb_value[column] for column in row] for row in map.splitlines()]

                fig = plt.figure(constrained_layout=True, figsize=(15, 15))
                fig.suptitle("Rossumoya Ecosystem Model", fontsize=35, fontweight="bold")
                fig.tight_layout(h_pad=1, w_pad=2)
                ax = fig.add_gridspec(5, 6)

                # Create Subplots
                ax1 = fig.add_subplot(ax[0, 0:2])
                ax1.set_title('Age Histogram', fontsize=20)
                ax2 = fig.add_subplot(ax[0, 2:4])
                ax2.set_title('Weight Histogram', fontsize=20)
                ax3 = fig.add_subplot(ax[0, 4:6])
                ax3.set_title("Fitness Histogram", fontsize=20)
                ax4 = fig.add_subplot(ax[1:3, 2:4])
                ax4.set_title("Island (Year: {num:03d})".format(num=year), fontsize=30, fontweight="bold")
                ax5 = fig.add_subplot(ax[3:, 0:])
                ax5.set_title("Animal Poplulation", fontsize=20)
                ax6 = fig.add_subplot(ax[1:3, 0:2])
                ax6.set_title("Herbivore Distribution", fontsize=20)
                ax7 = fig.add_subplot(ax[1:3, 4:])
                ax7.set_title("Carnivore Distribution", fontsize=20)

                # Create Island Map
                ax4.grid()
                ax4.imshow(map_rgb)
                ax4.set_xticks(range(len(map_rgb[0])))
                ax4.set_xticklabels(range(1, 1 + len(map_rgb[0])))
                ax4.set_yticks(range(len(map_rgb)))
                ax4.set_yticklabels(range(1, 1 + len(map_rgb)))

                water_patch = mpatches.Patch(color=(0.0, 0.0, 1.0), label="Water")
                desert_patch = mpatches.Patch(color=(1.0, 1.0, 0.5), label="Desert")
                highland_patch = mpatches.Patch(color=(0.5, 1.0, 0.5), label="Highland")
                lowland_patch = mpatches.Patch(color=(0.0, 0.6, 0.0), label="Lowland")
                ax4.legend(bbox_to_anchor=(0.5, -0.1), loc="upper center", mode="expand", ncol=2,
                           handles=[lowland_patch, highland_patch, desert_patch, water_patch], fontsize=10)

                # Create Herbivore Distribution Map
                herb_dist = ax6.imshow(h_heatmap, vmin=0, vmax=self.cmax_animals["Herbivore"])
                fig.colorbar(herb_dist, ax=ax6, location="left", shrink=0.5)
                ax6.set_xticks(range(len(map_rgb[0])))
                ax6.set_xticklabels(range(1, 1 + len(map_rgb[0])))
                ax6.set_yticks(range(len(map_rgb)))
                ax6.set_yticklabels(range(1, 1 + len(map_rgb)))
                ax6.grid()

                # Create Carnivore Distribution Map
                carn_dist = ax7.imshow(c_heatmap, vmin=0, vmax=self.cmax_animals["Carnivore"])
                ax7.grid()
                fig.colorbar(carn_dist, ax=ax7, location="right", shrink=0.5)
                ax7.set_xticks(range(len(map_rgb[0])))
                ax7.set_xticklabels(range(1, 1 + len(map_rgb[0])))
                ax7.set_yticks(range(len(map_rgb)))
                ax7.set_yticklabels(range(1, 1 + len(map_rgb)))

                # Create Animal Count per year
                ax5.plot(h_pop, color='g', label='Herbivore', lw=5)
                ax5.plot(c_pop, color='r', label='Cerbivore', lw=5)
                ax5.grid()
                ax5.set_ylim(0, self.ymax_animals)

                # Create Age, Weight and Fitness Histogram
                ax1.hist(h_age, bins=int(self.hist_specs["age"]["max"] // self.hist_specs["age"]["delta"]), color='g',
                         label='Herbivore', histtype="step", range=[0, self.hist_specs["age"]["max"]], lw=5)
                ax1.grid()

                ax2.hist(h_weight, bins=int(self.hist_specs["weight"]["max"] // self.hist_specs["weight"]["delta"]),
                         color='g', label='Herbivore', histtype="step", range=[0, self.hist_specs["weight"]["max"]], lw=5)
                ax2.grid()
                ax3.hist(h_fitness, bins=int(self.hist_specs["fitness"]["max"] // self.hist_specs["fitness"]["delta"]),
                         color='g', label='Herbivore', histtype="step", range=[0, self.hist_specs["weight"]["max"]], lw=5)
                ax3.grid()

                ax1.hist(c_age, bins=int(self.hist_specs["age"]["max"] // self.hist_specs["age"]["delta"]), color='r',
                         label="Carnivore", histtype="step", range=[0, self.hist_specs["age"]["max"]], lw=5)
                ax2.hist(c_weight, bins=int(self.hist_specs["weight"]["max"] // self.hist_specs["weight"]["delta"]),
                         color='r', label="Carnivore", histtype="step", range=[0, self.hist_specs["weight"]["max"]], lw=5)
                ax3.hist(c_fitness, bins=int(self.hist_specs["fitness"]["max"] // self.hist_specs["fitness"]["delta"]),
                         color='r', label="Carnivore", histtype="step", range=[0, self.hist_specs["fitness"]["max"]], lw=5)

                # Save File
                plt.savefig(plotfilename)
                plt.close()

