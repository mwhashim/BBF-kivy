from __future__ import division
import os, sys

from astropy.cosmology import wCDM
from astropy.io import fits

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.anchorlayout import AnchorLayout

from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserListView, FileChooserIconView
from kivy.uix.camera import Camera
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner


from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.behaviors import ToggleButtonBehavior

from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.progressbar import ProgressBar

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as mpimg
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
import matplotlib

import numpy as np
from matplotlib import cm, colors
from matplotlib.lines import Line2D

import glob
import subprocess, shlex

from textdictENG import text_dict


#from kivy.core.window import Window
#Window.clearcolor = (1, 1, 1, 1)

#--- CWD -----
CWD = os.getcwd(); dpi = 100

class AnchoredHScaleBar(matplotlib.offsetbox.AnchoredOffsetbox):
    """ size: length of bar in data units
        extent : height of bar ends in axes units """
    def __init__(self, size=1, extent = 0.02, label="", loc=2, ax=None, pad=0.4, borderpad=0.5, ppad = 0, sep=2, prop=None, frameon=True, **kwargs):
        if not ax:
            ax = plt.gca()
        trans = ax.get_xaxis_transform()
        size_bar = matplotlib.offsetbox.AuxTransformBox(trans)
        line = Line2D([0,size],[0,0], **kwargs)
        vline1 = Line2D([0,0],[-extent/2.,extent/2.], **kwargs)
        vline2 = Line2D([size,size],[-extent/2.,extent/2.], **kwargs)
        size_bar.add_artist(line)
        size_bar.add_artist(vline1)
        size_bar.add_artist(vline2)
        txt = matplotlib.offsetbox.TextArea(label, minimumdescent=False, textprops=dict(color="white", size=10))
        self.vpac = matplotlib.offsetbox.VPacker(children=[size_bar,txt], align="right", pad=ppad, sep=sep)
        matplotlib.offsetbox.AnchoredOffsetbox.__init__(self, loc, pad=pad, borderpad=borderpad, child=self.vpac, prop=prop, frameon=frameon)

class IconButton(ButtonBehavior, Image):
    pass

class MyApp(App):

    def build(self):
        
        #--:Initiating plot pan
        self.fig, self.ax, self.canvas = self.PlotPan()
        self.fig0, self.ax0, self.canvas0 = self.PlotPan()

        #--: Home Page
        self.img=mpimg.imread('BBF_frontpage.png')
        self.ax.imshow(self.img); self.anim_running = True; self.anim_compare = True
        
        #--: Widgets
        btn_user = IconButton(source='./icons/user.png', text='', size_hint_x=None, width=50)
        btn_user.bind(on_release=self.show_popup_user)
        
        btn_sim = IconButton(source='./icons/sim.png', size_hint_x = None, width = 50)
        btn_sim.bind(on_release=self.show_popup_sim)
        
        btn_lens = IconButton(source='./icons/lens.png', size_hint_x = None, width = 50)
        
        btn_settings = IconButton(source='./icons/settings.png', size_hint_x = None, width = 50)
        
        btn_home = IconButton(source='./icons/home.png', size_hint_x = None, width = 50)
        btn_home.bind(on_release=self.clean)
        
        self.btn_pause = IconButton(source='./icons/pause.png', size_hint_x = None, width = 50)
        self.btn_pause.bind(on_press=self.pause)
        
        self.btn_compare = IconButton(source='./icons/compare.ico', size_hint_x = None, width = 50)
        self.btn_compare.bind(on_press=self.compare)
        
        self.btn_sim_save = IconButton(source='./icons/save.png', size_hint_x = None, width = 50)
        self.btn_sim_save.bind(on_release=self.save_movie)

        #--:Page Layout
        #--- Page 1
        Pages = PageLayout(orientation= "vertical")
        self.Box_sim = BoxLayout(orientation= "horizontal")
        self.Box_sim.add_widget(self.canvas)
        Pages.add_widget(self.Box_sim)
        #--- Page 2
        self.Settings_Page = GridLayout(cols=1, row_force_default=True, row_default_height=40)
        
        self.Settings_Page.add_widget(btn_user)
        self.Settings_Page.add_widget(btn_sim)
        self.Settings_Page.add_widget(btn_lens)
        self.Settings_Page.add_widget(btn_settings)
        self.Settings_Page.add_widget(btn_home)
        
        Pages.add_widget(self.Settings_Page)
        return Pages
    
    def PlotPan(self):
        #--:PLot Pan
        fig = plt.Figure(facecolor='0.7', frameon=False)
        ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
        canvas = FigureCanvasKivyAgg(fig)
        return fig, ax, canvas
    
    def compare(self, *args):
        if self.anim_compare:
            self.Box_sim.add_widget(self.canvas0)
            self.anim_compare = False
        else:
            self.Box_sim.remove_widget(self.canvas0)
            self.anim_compare = True

    def show_popup_user(self,*args):
        label_name = Image(source='./icons/name.png')
        self.input_name = TextInput(text='', multiline=False, size_hint_x = None, width = 200)
        
        label_email = Image(source='./icons/email.png')
        input_email = TextInput(text='', multiline=False, size_hint_x = None, width = 200)
        
        self.btn_cam = IconButton(source='./icons/photo.png')
        self.btn_cam.bind(on_release=self.show_popup_cam)
        
        Settings_content = BoxLayout(orientation='horizontal')
        user_content = GridLayout(cols = 2, size_hint_y = None, height = '58dp')
        
        user_content.add_widget(label_name)
        user_content.add_widget(self.input_name)
        user_content.add_widget(label_email)
        user_content.add_widget(input_email)
        Settings_content.add_widget(user_content)
        Settings_content.add_widget(self.btn_cam)

        self.popup = Popup(title='', size_hint=(.640, .480), content=Settings_content, auto_dismiss=True)
        self.popup.open()
    
    def show_popup_sim(self,*args):
        
        self.btn_sim_start = IconButton(source='./icons/play.png', text='', size_hint_y = None, height = '48dp')
        self.btn_sim_start.bind(on_release=self.sim_start)
        
        image_dm = Image(source='./icons/dm.gif')
        image_de = Image(source='./icons/de.gif')
        
        self.slider_dm = Slider(min= 0.0, max= 1.0, value = 0.25, step = 0.25, orientation='vertical', value_track=True, value_track_color=[1, 0, 0, 1], size_hint_y = None, height = '160dp')
        self.slider_de = Slider(min= 0.0, max= 1.0, value = 0.75, step = 0.25, orientation='vertical', value_track=True, value_track_color=[1, 0, 0, 1], size_hint_y = None, height = '160dp')
        
        label_dm = Label(text = 'Dark Matter')
        label_de = Label(text = 'Dark Energy')
        label_png = Label(text = 'Early Universe')
        label_gvr = Label(text = 'Gravity Type')
        
        self.spinner_dm = Spinner(text='Select', values=('Cold', 'Warm'))
        self.spinner_de = Spinner(text='Select', values=('Constant', 'Quintessence', 'Phantom'))
        self.spinner_png = Spinner(text='Select', values=('Gaussian', 'Negative Non-Gaussain', 'Positive Non-Gaussian'))
        self.spinner_gvr = Spinner(text='Select', values=('Enistein', 'Modified Gravity'))
        
        Settings_content = BoxLayout(orientation='horizontal')
        
        slider_dm_content = GridLayout(cols=1)
        slider_dm_content.add_widget(image_dm)
        slider_dm_content.add_widget(self.slider_dm)
        
        
        slider_de_content = GridLayout(cols=1)
        slider_de_content.add_widget(image_de)
        slider_de_content.add_widget(self.slider_de)
        
        
        subSettings_content = GridLayout(cols=2, size_hint_x = None, width=350)
        subSettings_content.add_widget(label_dm)
        subSettings_content.add_widget(self.spinner_dm)
        subSettings_content.add_widget(label_de)
        subSettings_content.add_widget(self.spinner_de)
        subSettings_content.add_widget(label_png)
        subSettings_content.add_widget(self.spinner_png)
        subSettings_content.add_widget(label_gvr)
        subSettings_content.add_widget(self.spinner_gvr)
        
        Settings_content.add_widget(subSettings_content)
        Settings_content.add_widget(slider_dm_content)
        Settings_content.add_widget(slider_de_content)
        Settings_content.add_widget(self.btn_sim_start)

        
    
        self.popup_sim = Popup(title='', size_hint=(.680, .460), content=Settings_content, auto_dismiss=True)
        self.popup_sim.open()
    
    def show_popup_cam(self, *args):
        self.cam = Camera(resolution=(640, 480))
        content = BoxLayout(orientation='vertical')
        btn_capture = IconButton(source='./icons/shot.png', text='', size_hint_y = None, height = '48dp')
        btn_capture.bind(on_release=self.camera)
        
        content.add_widget(self.cam)
        content.add_widget(btn_capture)
        
        self.popup = Popup(title='', size_hint=(.600, .785), content=content, auto_dismiss=True)
        self.popup.open()
    
    def clean(self, *args):
        self.ax.clear(); self.ax.axis('off'); self.ax.imshow(self.img); self.canvas.draw();
        self.Settings_Page.remove_widget(self.btn_pause); self.Settings_Page.remove_widget(self.btn_compare)
        self.Settings_Page.remove_widget(self.btn_sim_save)
    
    def camera(self, *args):
        self.cam.play = not self.cam.play
        self.cam.export_to_png("./tmp/" + self.input_name.text + "_image.png")
        self.btn_cam.source = "./tmp/" + self.input_name.text + "_image.png"
    
    def sim_start(self, *args):
        #self.progress_var.set(0); self.frames = 0; self.maxframes = 0
        
        Simu_Dir = "./../Dens-Maps/"
        
        cosmo = wCDM(70.3, self.slider_dm.value, self.slider_de.value, w0 = -1.0)
        #filenames=sorted(glob.glob(self.simdir + "/" + Simu_Dir +'*.npy')); lga = linspace(log(0.05), log(1.0), 300); a = exp(lga); z = 1./a - 1.0;
        #lktime = z #cosmo.lookback_time(z).value
        filenames=sorted(glob.glob(Simu_Dir + '*.npy')); lga = np.linspace(np.log(0.05), np.log(1.0), 300); a = np.exp(lga); z = 1./a - 1.0; lktime = cosmo.lookback_time(z).value
        def animate(filename):
            image = np.load(filename); indx = filenames.index(filename)#; image=ndimage.gaussian_filter(image, sigma= sigmaval, truncate=truncateval, mode='wrap')
            im.set_data(image + 1)#; im.set_clim(image.min()+1.,image.max()+1.)
            self.time.set_text('%s %s' %(round(lktime[indx], 4), text_dict['t49']))
            return im
        
        dens_map = np.load(filenames[0])#;  dens_map=ndimage.gaussian_filter(dens_map, sigma= sigmaval, truncate=truncateval, mode='wrap') #; dens_map0 = load(filenames[-1]); #print dens_map0.min()+1, dens_map0.max()+1.
        im = self.ax.imshow(dens_map + 1, cmap=cm.magma, norm=colors.LogNorm(vmin=1., vmax=1800., clip = True), interpolation="bicubic")#, clim = (1, 1800.+1.))
        

        self.time = self.ax.text(0.1, 0.05 , text_dict['t43'] + ' %s Gyr' %round(lktime[0], 4), horizontalalignment='left', verticalalignment='top',color='white', transform = self.ax.transAxes, fontsize=10)


        arr_hand = mpimg.imread(CWD + "/tmp/" + self.input_name.text +  "_image.png")
        imagebox = OffsetImage(arr_hand, zoom=.1); xy = (0.1, 0.15) # coordinates to position this image

        ab = AnnotationBbox(imagebox, xy, xybox=(0.1, 0.15), xycoords='axes fraction', boxcoords='axes fraction', pad=0.1)
        self.ax.add_artist(ab)

        
        arr_hand1 = mpimg.imread("./icons/simcode.png")
        imagebox1 = OffsetImage(arr_hand1, zoom=.1); xy = (0.9, 0.9) # coordinates to position this image
        ab1 = AnnotationBbox(imagebox1, xy, xybox=(0.9, 0.9), xycoords='axes fraction', boxcoords='axes fraction', pad=0.1)
        self.ax.add_artist(ab1)

        #iMpc = lambda x: x*1024/125  #x in Mpc, return in Pixel *3.085e19
        ob = AnchoredHScaleBar(size=0.1, label="10Mpc", loc=4, frameon=False, pad=0.6, sep=2, color="white", linewidth=0.8)
        self.ax.add_artist(ob)

#        sim_details_text = '%s: %s\n%s: %s\n%s: %s\n%s: %s\n%s: %s\n%s: %s' %(text_dict['t42'], self.Name_Var.get(), text_dict['t53'], self.SC_Type, text_dict['t20'], self.DE_type, text_dict['t24'], self.DM_type, text_dict['t27'],  self.EU_Type, text_dict['t31'] , self.MG_Type)

        sim_details_text = '%s: %s\n%s: %s\n%s: %s\n%s: %s\n%s: %s' %(text_dict['t42'], self.input_name.text, text_dict['t53'], self.spinner_de.text, text_dict['t24'], self.spinner_dm.text, text_dict['t27'],  self.spinner_png.text, text_dict['t31'] , self.spinner_gvr.text) #, self.SC_Type, text_dict['t20']
        print sim_details_text
        self.ax.text(0.1, 0.83, sim_details_text, color='white', bbox=dict(facecolor='none', edgecolor='white', boxstyle='round,pad=1', alpha=0.5), transform = self.ax.transAxes, alpha = 0.5)

        self.ani = animation.FuncAnimation(self.fig, animate, filenames, repeat=False, interval=25, blit=False)
        self.ax.axis('off'); self.ax.get_xaxis().set_visible(False); self.ax.get_yaxis().set_visible(False); self.canvas.draw()
        
#        self.progress["value"] = 0; self.maxframes = 300; self.progress["maximum"] = 300
#        self.read_frames()
        self.Settings_Page.add_widget(self.btn_pause)
        self.Settings_Page.add_widget(self.btn_compare)
        self.Settings_Page.add_widget(self.btn_sim_save)
        self.popup_sim.dismiss()
        
    def pause(self, *args):
        if self.anim_running:
            self.btn_pause.source = './icons/play.png'
            self.ani.event_source.stop()
            self.anim_running = False
        else:
            self.btn_pause.source = './icons/pause.png'
            self.ani.event_source.start()
            self.anim_running = True

    def save_movie(self, *args):
        writer = animation.writers['ffmpeg'](fps=15)#, bitrate=16000, codec='libx264')
        
#        self.ani.save(self.savedir + "/" + self.img_filename + "_movie.mp4", writer=writer, dpi=dpi) #, savefig_kwargs={'dpi' : 200}
#        video_file = self.savedir + "/" + self.img_filename + "_movie.mp4"
#        muxvideo_file = self.savedir + "/" + self.img_filename + "_mux_movie.mp4"
#
        self.ani.save(self.input_name.text + "_movie.mp4", writer=writer, dpi=dpi) #, savefig_kwargs={'dpi' : 200}
        video_file = self.input_name.text + "_movie.mp4"
        muxvideo_file = self.input_name.text + "_mux_movie.mp4"
        
        audio_file = "ChillingMusic.wav"
        cmd = 'ffmpeg -i '+ video_file + ' -i ' + audio_file + ' -shortest ' + muxvideo_file
        subprocess.call(cmd, shell=True); print('Saving and Muxing Done')
        self.muxvideo = self.input_name.text + "_mux_movie.mp4"

#--------- RUN ----------------------------
if __name__ == "__main__":
    MyApp().run()

