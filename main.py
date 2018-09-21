from __future__ import division
import os, sys

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

from kivy.uix.behaviors import ButtonBehavior

from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.progressbar import ProgressBar

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as mpimg
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
import matplotlib

#from astropy.cosmology import wCDM
#from astropy.io import fits

import numpy as np
from matplotlib import cm, colors
from matplotlib.lines import Line2D

import glob


#from kivy.core.window import Window
#Window.clearcolor = (1, 1, 1, 1)

#--- CWD -----
CWD = os.getcwd()

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
        #--:PLot Pan
        self.fig = plt.Figure(facecolor='0.7', frameon=False)
        self.ax = plt.Axes(self.fig, [0., 0., 1., 1.]); self.ax.set_axis_off(); self.fig.add_axes(self.ax)
        self.canvas = FigureCanvasKivyAgg(self.fig)
        self.img=mpimg.imread('BBF_frontpage.png')
        self.ax.imshow(self.img)
        
        #--: Widgets
#        btn_cam = IconButton(source='./icons/cam.png', size_hint_x = None, width = 50)
#        btn_cam.bind(on_release=self.show_popup_cam)

        btn_user = IconButton(source='./icons/user.png', text='', size_hint_x=None, width=50)
        btn_user.bind(on_release=self.show_popup_user)
        
        btn_sim = IconButton(source='./icons/sim.png', size_hint_x = None, width = 50)
        btn_sim.bind(on_release=self.show_popup_sim)
        
        btn_lens = IconButton(source='./icons/lens.jpg', size_hint_x = None, width = 50)
        btn_home = IconButton(source='./icons/simcode.png', size_hint_x = None, width = 50)
        btn_home.bind(on_release=self.clean)
        
        fichoo = FileChooserIconView(size_hint_y = 0.8)
        
        btn_sim_start = IconButton(source='./icons/play.png', text='', size_hint_x=None, width=50)
        btn_sim_start.bind(on_release=self.start)
        
        label_name = Label(text='Name')
        input_name = TextInput(text='Name', multiline=False)
        
        pb = ProgressBar(max=1000)
        # this will update the graphics automatically (75% done)
        pb.value = 750

        #--:Page Layout
        #--- Page 1
        Pages = PageLayout(orientation= "vertical")
        Pages.add_widget(self.canvas)
        #--- Page 2
        Settings_Page = GridLayout(cols=1, row_force_default=True, row_default_height=40)
        
        Settings_Page.add_widget(btn_user)
        Settings_Page.add_widget(btn_sim)
        Settings_Page.add_widget(btn_lens)
        Settings_Page.add_widget(btn_sim_start)
        Settings_Page.add_widget(btn_home)
        
        #Settings_Page.add_widget(fichoo)

        
        #Settings_Page.add_widget(textinput)
        #Settings_Page.add_widget(pb)
        Pages.add_widget(Settings_Page)
        return Pages
    
    def show_popup_user(self,*args):
        label_name = Image(source='./icons/name.png')
        self.input_name = TextInput(text='', multiline=False, size_hint_x = None, width = 350)
        
        label_email = Image(source='./icons/email.png')
        input_email = TextInput(text='', multiline=False, size_hint_x = None, width = 350)
        
        
        btn_cam = IconButton(source='./icons/cam.png')
        btn_cam.bind(on_release=self.show_popup_cam)
        
        self.label_photo = Image(source='./icons/photo.png', size_hint_y = None,  width = 350)
        
        Settings_content = GridLayout(cols=2, spacing = [20,0])
        Settings_content.add_widget(label_name)
        Settings_content.add_widget(self.input_name)
        Settings_content.add_widget(label_email)
        Settings_content.add_widget(input_email)
        Settings_content.add_widget(btn_cam)
        Settings_content.add_widget(self.label_photo)
        
        self.popup = Popup(title='', size_hint=(.550, .400), content=Settings_content, auto_dismiss=True)
        self.popup.open()
    
    def show_popup_sim(self,*args):
        label_name = Label(text='Name')
        input_name = TextInput(text='Name', multiline=False)
        Settings_content = GridLayout(cols=2, row_force_default=True, row_default_height=40)
        Settings_content.add_widget(label_name)
        Settings_content.add_widget(input_name)
    
        self.popup = Popup(title='', size_hint=(.600, .785), content=Settings_content, auto_dismiss=True)
        self.popup.open()
    
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
        self.ax.clear(); self.ax.axis('off'); self.ax.imshow(self.img); self.canvas.draw()
    
    def camera(self, *args):
        self.cam.play = not self.cam.play
        #timestr = time.strftime("%Y%m%d_%H%M%S")
        self.cam.export_to_png("./tmp/image.png")
        self.label_photo.source = "./tmp/image.png"
    
    def start(self, *args):
        #self.progress_var.set(0); self.frames = 0; self.maxframes = 0
        
        Simu_Dir = "./../Dens-Maps/"
        
        #cosmo = wCDM(70.3, self.Omega_m_Var.get(), self.Omega_l_Var.get(), w0=self.wx)
        #filenames=sorted(glob.glob(self.simdir + "/" + Simu_Dir +'*.npy')); lga = linspace(log(0.05), log(1.0), 300); a = exp(lga); z = 1./a - 1.0;
        #lktime = z #cosmo.lookback_time(z).value
        filenames=sorted(glob.glob(Simu_Dir + '*.npy')); lga = np.linspace(np.log(0.05), np.log(1.0), 300); a = np.exp(lga); z = 1./a - 1.0;
        lktime = z #cosmo.lookback_time(z).value
        def animate(filename):
            image = np.load(filename); indx = filenames.index(filename)#; image=ndimage.gaussian_filter(image, sigma= sigmaval, truncate=truncateval, mode='wrap')
            im.set_data(image + 1)#; im.set_clim(image.min()+1.,image.max()+1.)
            #self.time.set_text('%s %s' %(round(lktime[indx], 4), text_dict['t49']))
            self.time.set_text('%s %s' %(round(lktime[indx], 4), 'time: '))
            return im
        
        dens_map = np.load(filenames[0])#;  dens_map=ndimage.gaussian_filter(dens_map, sigma= sigmaval, truncate=truncateval, mode='wrap') #; dens_map0 = load(filenames[-1]); #print dens_map0.min()+1, dens_map0.max()+1.
        im = self.ax.imshow(dens_map + 1, cmap=cm.magma, norm=colors.LogNorm(vmin=1., vmax=1800., clip = True), interpolation="bicubic")#, clim = (1, 1800.+1.))
        
        self.ax.annotate('This Universe is made by ' + self.input_name.text, xy=(0.25, 0.45), fontsize='12', fontstyle = 'oblique', color='white', xycoords='data', xytext=(10., 40.), textcoords='data')
        self.time = self.ax.text(0.1, 0.05 , 'time' + ' %s Gyr' %round(z[0], 4), horizontalalignment='left', verticalalignment='top',color='white', transform = self.ax.transAxes, fontsize=10)


        arr_hand = mpimg.imread(CWD + "/tmp/" + "image.png")
        imagebox = OffsetImage(arr_hand, zoom=.08); xy = [0.30, 0.45] # coordinates to position this image

        ab = AnnotationBbox(imagebox, xy, xybox=(50., -70.), xycoords='data', boxcoords="offset points", pad=0.1)
        self.ax.add_artist(ab)

        
        arr_hand1 = mpimg.imread("./icons/simcode.png")
        imagebox1 = OffsetImage(arr_hand1, zoom=.1); xy = [950.0, 85.0] # coordinates to position this image
        ab1 = AnnotationBbox(imagebox1, xy, xybox=(0., 0.), xycoords='data', boxcoords="offset points", pad=0.1)
        self.ax.add_artist(ab1)

        #iMpc = lambda x: x*1024/125  #x in Mpc, return in Pixel *3.085e19
        ob = AnchoredHScaleBar(size=0.1, label="10Mpc", loc=4, frameon=False, pad=0.6, sep=2, color="white", linewidth=0.8)
        self.ax.add_artist(ob)

#        sim_details_text = '%s: %s\n%s: %s\n%s: %s\n%s: %s\n%s: %s\n%s: %s' %(text_dict['t42'], self.Name_Var.get(), text_dict['t53'], self.SC_Type, text_dict['t20'], self.DE_type, text_dict['t24'], self.DM_type, text_dict['t27'],  self.EU_Type, text_dict['t31'] , self.MG_Type)
#        print sim_details_text
#        self.ax.text(0.18, 0.85, sim_details_text, color='white', bbox=dict(facecolor='none', edgecolor='white', boxstyle='round,pad=1', alpha=0.5), transform = self.ax.transAxes, alpha = 0.5)

        self.ani = animation.FuncAnimation(self.fig, animate, filenames, repeat=False, interval=25, blit=False)
        self.ax.axis('off'); self.ax.get_xaxis().set_visible(False); self.ax.get_yaxis().set_visible(False); self.canvas.draw()
        
#        self.progress["value"] = 0; self.maxframes = 300; self.progress["maximum"] = 300
#        self.read_frames()


#--------- RUN ----------------------------
if __name__ == "__main__":
    MyApp().run()

