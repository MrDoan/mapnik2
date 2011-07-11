#!/usr/bin/python
#
# Generates a single large PNG image for a UK bounding box
# Tweak the lat/lon bounding box (ll) and image dimensions
# to get an image of arbitrary size.
#
# To use this script you must first have installed mapnik2
# and imported a planet file into a Postgres DB using
# osm2pgsql.
#
# Note that mapnik renders data differently depending on
# the size of image. More detail appears as the image size
# increases but note that the text is rendered at a constant
# pixel size so will appear smaller on a large image.
#
# Based on generate_image.py from OSM (http://svn.openstreetmap.org/applications/rendering/mapnik/generate_image.py)

import mapnik2
import sys, os
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate image using Mapnik2')
    parser.add_argument('--mapfile', required=True, help="Mapnik2 XML file")
    parser.add_argument('--zoom', type=int, default=7, choices=range(1, 19), help="Zoom level [1-18]" )
    parser.add_argument('--bbox', type=float, nargs=4, required=True, help="Define bounding box WGS84")
    args = parser.parse_args()

    map_uri = args.mapfile.partition('.')[0] + ".png"

    #---------------------------------------------------
    #  Change this to the bounding box you want
    #
    #ll = (-5.2, 41.4, 10.16, 46.2)
    #ll = (1.393547058105469, 43.56610697474913, 1.429810523986817, 43.58131079720606) #reynerie
    #ll = (1.406988241528325, 43.56730920511517, 1.461919882153325, 43.60237411394007) #ponts
    #ll = (1.359014509180042, 43.59232959871322, 1.404848096826527, 43.62626162214223) #tournefeuille (rocades)
    ll = args.bbox
    #---------------------------------------------------

    z = args.zoom
    imgx = 500 * z
    imgy = 1000 * z

    m = mapnik2.Map(imgx,imgy)
    mapnik2.load_map(m,args.mapfile)
    prj = mapnik2.Projection("+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over")
    c0 = prj.forward(mapnik2.Coord(ll[0],ll[1]))
    c1 = prj.forward(mapnik2.Coord(ll[2],ll[3]))
    if hasattr(mapnik2,'mapnik_version') and mapnik2.mapnik_version() >= 800:
        bbox = mapnik2.Box2d(c0.x,c0.y,c1.x,c1.y)
    else:
        bbox = mapnik2.Envelope(c0.x,c0.y,c1.x,c1.y)
    m.zoom_to_box(bbox)
    im = mapnik2.Image(imgx,imgy)
    mapnik2.render(m, im)
    view = im.view(0,0,imgx,imgy) # x,y,width,height
    view.save(map_uri,'png')
