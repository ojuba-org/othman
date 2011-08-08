# -*- coding: UTF-8 -*-
"""
Othman - Quran browser
gtkUi - gtk user interface for Othman API

Copyright © 2008-2010, Muayyad Alsadi <alsadi@ojuba.org>

    Released under terms of Waqf Public License.
    This program is free software; you can redistribute it and/or modify
    it under the terms of the latest version Waqf Public License as
    published by Ojuba.org.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

    The Latest version of the license can be found on
    "http://waqf.ojuba.org/license"

"""
import sys, os, os.path, time
import gettext
import pango
import glib
import gtk

from core import othmanCore, searchIndexer

class searchWindow(gtk.Window):
  def __init__(self, w):
    gtk.Window.__init__(self)
    self.w=w
    self.connect('delete-event', lambda w,*a: w.hide() or True)
    self.last_txt = None
    self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_UTILITY)
    self.set_modal(True)
    self.set_deletable(True)
    self.set_title(_('Search results'))
    self.set_transient_for(w)
    vb=gtk.VBox(False,0); self.add(vb)
    self.search=gtk.Entry()
    self.search.set_width_chars(15)
    vb.pack_start(self.search, False,False, 0)
    self.scroll=gtk.ScrolledWindow()
    self.scroll.set_policy(gtk.POLICY_NEVER,gtk.POLICY_ALWAYS)
    vb.pack_start(self.scroll,True, True, 6)
    
    self.ls = gtk.ListStore(int,str,int,int)
    self.cells=[]; self.cols=[]
    self.cells.append(gtk.CellRendererText())
    self.cols.append(gtk.TreeViewColumn(_('Sura'), self.cells[0], text=1))
    self.cols[0].set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    self.cols[0].set_resizable(True)

    self.cells.append(gtk.CellRendererText()); # self.cols[-1].set_expand(False)
    self.ls_w=gtk.TreeView(self.ls)
    self.ls_w.connect("cursor-changed", self.move)
    self.ls_w.set_headers_visible(False)
    for i in self.cols: self.ls_w.insert_column(i, -1)
    self.scroll.add(self.ls_w)
    self.search.connect("activate", self.search_cb)
    self.show_all()

  def move(self, t):
    a=self.ls_w.get_selection().get_selected()
    if not a or len(a)<2 or not a[1]: return
    sa=self.ls[self.ls.get_path(a[1])[0]]
    self.w.sura_c.set_active(sa[2]-1)
    self.w.viewAya(sa[3], sa[2])

  def search_cb(self, b, *a):
    t=b.get_text()
    self.w.search.set_text(t)
    self.find(t)

  def find(self, txt, backward=False):
    txt=txt.strip()
    if not txt: self.hide(); return
    if type(txt)==str: txt=txt.decode('utf-8')
    if txt==self.last_txt:
      # TODO: just move cursor to next/prev result before showing it
      pass
    else:
      self.search.set_text(txt)
      self.last_txt=txt
      self.ls.clear()
      for i in self.w.ix.findPartial(txt.split()):
        sura,aya=self.w.suraAyaFromAyaId(i)
        name=self.w.suraInfoById[sura-1][0]
        self.ls.append([i, "%03d %s - %03d" % (sura, name, aya), sura, aya,])
      self.ls_w.set_cursor((0,))
    self.show_all()

class othmanUi(gtk.Window, othmanCore):
  def __init__(self):
    gtk.window_set_default_icon_name('Othman')
    gtk.Window.__init__(self)
    othmanCore.__init__(self)
    self.sw = None
    self.lastSearchText=None
    self.lastSearchResult=[]
    self.ix=searchIndexer()
    self.set_title(_('Othman Quran Browser'))
    self.connect("delete_event", self.quit)
    self.set_default_size(600, 480)

    self.clip1=gtk.Clipboard(selection="PRIMARY")
    self.clip2=gtk.Clipboard(selection="CLIPBOARD")
    self.accel=gtk.AccelGroup()

    vb=gtk.VBox(False,0); self.add(vb)
    hb=gtk.HBox(False,2)
    vb.pack_start(hb,False, False, 0)

    self.scroll=gtk.ScrolledWindow()
    self.scroll.set_policy(gtk.POLICY_NEVER,gtk.POLICY_ALWAYS)
    self.scroll.connect_after("size-allocate", self.resize_cb)
    vb.pack_start(self.scroll,True, True, 6)

    img=gtk.Image()
    img.set_from_stock(gtk.STOCK_COPY,gtk.ICON_SIZE_BUTTON)
    b=gtk.Button()
    b.add(img)
    b.connect("clicked", self.show_cp_dlg)
    hb.pack_start(b,False, False, 0)
    hb.pack_start(gtk.VSeparator(),False, False, 6)
    hb.pack_start(gtk.Label(_("Sura")),False, False, 0)

    self.sura_ls=tuple("%d. %s" % (i+1,j[0]) for (i,j) in enumerate(self.suraInfoById))
    self.sura_c = gtk.combo_box_new_text()
    self.sura_c.set_wrap_width(5)
    for i in self.sura_ls: self.sura_c.append_text(i)
    self.sura_c.set_tooltip_text(_("choose a Sura"))
    self.sura_c.connect("changed", self.sura_changed_cb)
    hb.pack_start(self.sura_c,False, False, 0)

    hb.pack_start(gtk.VSeparator(),False, False, 6)
    img=gtk.Image()
    img.set_from_stock(gtk.STOCK_ZOOM_IN, gtk.ICON_SIZE_BUTTON)
    b=gtk.Button()
    b.add(img)
    hb.pack_start(b, False, False, 0)
    b.connect("clicked", self.zoomIn)
    
    img=gtk.Image()
    img.set_from_stock(gtk.STOCK_ZOOM_OUT, gtk.ICON_SIZE_BUTTON)
    b=gtk.Button()
    b.add(img)
    hb.pack_start(b, False, False, 0)
    b.connect("clicked", self.zoomOut)

    img=gtk.Image()
    img.set_from_stock(gtk.STOCK_MEDIA_FORWARD, gtk.ICON_SIZE_BUTTON)
    b=gtk.ToggleButton()
    b.add(img)
    hb.pack_start(b, False, False, 0)
    self.autoScrolling=False
    b.connect("clicked", self.autoScrollCb)
    glib.timeout_add(100, self.autoScroll, b)

    hb.pack_start(gtk.VSeparator(), False, False, 6)
    hb.pack_start(gtk.image_new_from_stock(gtk.STOCK_FIND, gtk.ICON_SIZE_BUTTON), False, False, 0)
    search=gtk.Entry(); search.set_width_chars(15)
    hb.pack_start(search, False,False, 0)
    search.connect("activate", self.search_cb)
    self.search=search

    hb.pack_start(gtk.VSeparator(),False, False, 6)
    img=gtk.Image()
    img.set_from_stock(gtk.STOCK_ABOUT, gtk.ICON_SIZE_BUTTON)
    b=gtk.Button()
    b.add(img)
    hb.pack_start(b, False, False, 0)
    b.connect("clicked", self.about)


    self.scale=1
    self.txt = gtk.ListStore(str,int,str)
    self.cells=[]; self.cols=[]
    self.cells.append(gtk.CellRendererText())
    #self.cols.append(gtk.TreeViewColumn('Quranic Text', self.cells[0], markup=0))
    self.cols.append(gtk.TreeViewColumn('Quranic Text', self.cells[0], text=0, foreground=2))
    self.cells[0].set_property("background","#fffff8")
    #self.cells[0].set_property("foreground","#204000")
    #self.cells[0].set_property("alignment",pango.ALIGN_CENTER)
    self.cells[0].set_property("wrap-mode",pango.WRAP_WORD_CHAR)
    self.cells[0].set_property("wrap-width",500)
    self.cells[0].set_property("font","Simplified Naskh 32")
    #self.cells[0].set_property("font","KFGQPC Uthmanic Script HAFS 32")
    self.cells[0].set_property("scale", self.scale)
    self.cols[0].set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

    self.cells.append(gtk.CellRendererText()); # self.cols[-1].set_expand(False)
    self.txt_list=gtk.TreeView(self.txt)
    self.txt_list.set_headers_visible(False)
    for i in self.cols: self.txt_list.insert_column(i, -1)

    self.scroll.add(self.txt_list)
    self.sura_c.set_active(0)
    self.build_cp_dlg()
    self.build_about_dlg()
    self.show_all()

  def build_about_dlg(self):
    self.about_w=gtk.AboutDialog()
    self.about_w.set_default_response(gtk.RESPONSE_CLOSE)
    self.about_w.connect('delete-event', lambda w,*a: w.hide() or True)
    self.about_w.connect('response', lambda w,*a: w.hide() or True)
    try: self.about_w.set_program_name("Othman")
    except: pass
    self.about_w.set_name(_('Othman Quran Browser'))
    #self.about_w.set_version(version)
    self.about_w.set_copyright("Copyright © 2008-2010 Muayyad Saleh Alsadi <alsadi@ojuba.org>")
    self.about_w.set_comments(_("Electronic Mus-haf"))
    self.about_w.set_license("""
    Released under terms of Waqf Public License.
    This program is free software; you can redistribute it and/or modify
    it under the terms of the latest version Waqf Public License as
    published by Ojuba.org.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

    The Latest version of the license can be found on
    "http://waqf.ojuba.org/"

""")
    self.about_w.set_website("http://othman.ojuba.org/")
    self.about_w.set_website_label("http://othman.ojuba.org")
    self.about_w.set_authors(["Muayyad Saleh Alsadi <alsadi@ojuba.org>"])
    self.about_w.set_translator_credits(_("translator-credits"))
    fn=os.path.join(self.data_dir, "quran-kareem.svg")
    try: logo=gtk.gdk.pixbuf_new_from_file_at_size(fn, 128, 128)
    except:
      fn=os.path.join(self.data_dir, "quran-kareem.png")
      logo=gtk.gdk.pixbuf_new_from_file(fn)
    self.about_w.set_logo(logo)


  def about(self, b):
    self.about_w.show_all()

  def search_cb(self, b, *a):
    if not self.sw: self.sw = searchWindow(self)
    self.sw.find(b.get_text())

  def autoScroll(self, b):
    if not self.autoScrolling: return True
    v=self.scroll.get_vadjustment()
    m=v.upper-v.page_size
    n=min(m, v.get_value() + 2 )
    if n==m: b.set_active(False)
    v.set_value(n)
    return True

  def autoScrollCb(self, b, *a):
    self.autoScrolling=b.get_active()

  def zoomIn(self, *a):
    sura,aya=self.getCurrentSuraAya()
    self.scale+=0.1
    self.cells[0].set_property("scale", self.scale)
    self.resize_cb()
    self.queue_draw()
    self.viewSura(sura)
    self.viewAya(aya)

  def zoomOut(self, *a):
    sura,aya=self.getCurrentSuraAya()
    self.scale-=0.1
    self.scale=max(0.2, self.scale)
    self.cells[0].set_property("scale", self.scale)
    self.resize_cb()
    self.queue_draw()
    self.viewSura(sura)
    self.viewAya(aya)

  def viewAya(self, aya, sura=None):
    if sura==None: sura=self.sura_c.get_active()+1
    aya=max(1,abs(aya))
    i=aya+int(self.showSunnahBasmala(sura))
    self.txt_list.scroll_to_cell((i-1,))
    self.txt_list.get_selection().select_path((i-1,))

  def viewSura(self, i):
    #self.play_pause.set_active(False)
    self.txt.clear()
    if self.showSunnahBasmala(i):
      #self.txt.append(['<span foreground="#440000">%s</span>' % self.basmala,0,])
      self.txt.append([self.basmala,0,"#802000",])
    for j,k in enumerate(self.getSuraIter(i)):
      self.txt.append([k[0],j+1,"#204000",])
    self.resize_cb()
    self.scroll.get_vadjustment().set_value(0)
    self.txt_list.get_selection().select_path((0,))

  def sura_changed_cb(self, c, *a):
    self.viewSura(self.sura_c.get_active()+1)

  def resize_cb(self,*args):
    if self.cols[0].get_width()>10: self.cells[0].set_property("wrap-width",self.cols[0].get_width()-10)

  def cp_cb(self, *a):
    sura=self.cp_sura.get_active()+1
    aya1=self.cp_from.get_value()
    aya2=self.cp_to.get_value()
    n=aya2-aya1+1
    i=self.cp_is_imlai.get_active()
    a=[' ','\n',' * ', ' *\n']
    s=a[int(i)*2+int(self.cp_aya_perline.get_active())]
    s=s.join([l[i] for l in self.getSuraIter(sura, n, aya1)])+'\n'
    self.clip1.set_text(s)
    self.clip2.set_text(s)
    self.cp_w.hide()

  def cp_sura_cb(self, *a):
    sura=self.cp_sura.get_active()+1
    m=self.suraInfoById[sura-1][5]
    self.cp_from.set_range(1, m)
    self.cp_to.set_range(1, m)
    self.cp_from.set_value(1)
    self.cp_to.set_value(m)

  def show_cp_dlg(self, *a):
    sura,aya=self.getCurrentSuraAya()
    aya=max(1, abs(aya))
    self.cp_sura.set_active(sura-1)
    self.cp_sura_cb()
    self.cp_from.set_value(aya)
    self.cp_w.show_all()

  def build_cp_dlg(self):
    self.cp_w = gtk.Window()
    self.cp_w.set_title(_('Copy to clipboard'))
    self.cp_w.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
    self.cp_w.connect('delete-event', lambda w,*a: w.hide() or True)
    self.cp_sura = gtk.combo_box_new_text(); self.cp_sura.set_wrap_width(5)

    for i in self.sura_ls: self.cp_sura.append_text(i)
    self.cp_sura.set_tooltip_text(_("choose a Sura"))
    
    self.cp_from=gtk.SpinButton(gtk.Adjustment(0, 0, 286, 1, 10, 0))
    self.cp_to=gtk.SpinButton(gtk.Adjustment(0, 0, 286, 1, 10, 0))
    self.cp_is_imlai=gtk.CheckButton(_("Imla'i style"))
    self.cp_aya_perline=gtk.CheckButton(_("an Aya per line"))
    self.cp_ok=gtk.Button(stock=gtk.STOCK_OK)
    self.cp_cancel=gtk.Button(stock=gtk.STOCK_CANCEL)
    vb=gtk.VBox(False,0)
    self.cp_w.add(vb)
    hb=gtk.HBox(False,3)
    vb.pack_start(hb,True,True,3)
    hb.pack_start(gtk.Label("سورة"),False,False,3)
    hb.pack_start(self.cp_sura,False,False,6)
    hb=gtk.HBox(False,6)
    vb.pack_start(hb,True,True,6)
    hb.pack_start(gtk.Label("الآيات من"),False,False,3)
    hb.pack_start(self.cp_from,False,False,3)
    hb.pack_start(gtk.Label("إلى"),False,False,3)
    hb.pack_start(self.cp_to,False,False,3)
    hb=gtk.HBox(False,6)
    vb.pack_start(hb,True,True,6)
    hb.pack_start(self.cp_is_imlai,False,False,3)
    hb.pack_start(self.cp_aya_perline,False,False,3)
    hb=gtk.HBox(False,6)
    vb.pack_start(hb,True,True,6)
    hb.pack_start(self.cp_ok,False,False,6)
    hb.pack_start(self.cp_cancel,False,False,6)
    self.cp_sura.connect("changed", self.cp_sura_cb)
    self.cp_cancel.connect('clicked', lambda *args: self.cp_w.hide())
    self.cp_ok.connect('clicked', self.cp_cb)
    self.cp_is_imlai.set_active(True)

  def getCurrentSuraAya(self):
    a=self.txt_list.get_selection().get_selected()
    aya=1
    if a: aya=self.txt[self.txt.get_path(a[1])[0]][1]
    aya=max(aya,1)
    return self.sura_c.get_active()+1, aya

  def quit(self,*args):
     gtk.main_quit()
     return False

def main():
  exedir=os.path.dirname(sys.argv[0])
  ld=os.path.join(exedir, 'locale')
  if not os.path.exists(ld): ld=os.path.join(exedir,'..','share','locale')
  gettext.install('othman', ld, unicode=0)
  w=othmanUi()
  gtk.main()

if __name__ == "__main__":
  main()

