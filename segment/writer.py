# MIT License
# 
# Copyright (c) 2022 MEng-Team-Project
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Custom writer module which takes output from the Yolo model and writes it
to an SQLite database. Refer to issue:
https://github.com/MEng-Team-Project/yolov7-segmentation/issues/1 for full
details."""

import sqlite3
import pathlib
import os


class Writer(object):
    def __init__(self, analysis_db_path):
        # Primary Key counters
        self.base_count     = 0
        self.tracked_count  = 0
        self.route_count    = 0
        self.subroute_count = 0
        
        # SQLite connection and cursor
        self.con = sqlite3.connect(analysis_db_path)
        self.cur = self.con.cursor()

        # Create Tables
        parent_dir = pathlib.Path(__file__).parent.resolve()
        sql_commands_path = \
            os.path.join(parent_dir, "./CREATE_TABLES.sql")
        with open(sql_commands_path) as f:
            sql_commands = f.read().split(";")
            for sql_command in sql_commands:
                command = sql_command + ";"
                print(command)
                self.cur.execute(command)

    def insert_base(
        self,
        frame,
        class_idx,
        x1,
        y1,
        x2,
        y2,
        conf):
        cmd = f"""INSERT INTO detections VALUES (
            {self.base_count},
            {frame},
            {class_idx},
            {x1},
            {y1},
            {x2},
            {y2},
            {conf}
        )"""
        self.cur.execute(cmd)
        self.base_count += 1

    def insert_info(
        self,
        frame,
        bbox_x1,
        bbox_y1,
        bbox_x2,
        bbox_y2,
        label,
        anchor_x,
        anchor_y):
        cmd = f"""INSERT INTO tracked VALUES (
            {self.tracked_count},
            {frame},
            {bbox_x1},
            {bbox_y1},
            {bbox_x2},
            {bbox_y2},
            {label},
            {anchor_x},
            {anchor_y}
        )"""
        self.cur.execute(cmd)
        self.tracked_count += 1

    def insert_route(
        self,
        frame,
        route_idx):
        cmd = f"""INSERT INTO routes VALUES (
            {self.route_count},
            {frame},
            {route_idx}
        )"""
        self.cur.execute(cmd)
        self.route_count += 1
        return self.route_count - 1 # Return this route count

    def insert_sub_route(
        self,
        route_id,
        x1,
        y1,
        x2,
        y2):
        cmd = f"""INSERT INTO route VALUES (
            {self.subroute_count},
            {route_id},
            {x1},
            {y1},
            {x2},
            {y2}
        )"""
        self.cur.execute(cmd)
        self.subroute_count += 1

    def begin(self):
        """Call this to begin the SQLite transaction."""
        self.cur.execute("BEGIN;")

    def end(self):
        """Call this to end the SQLite transaction and close
        the SQLite connection."""
        self.cur.execute("COMMIT;")
        self.con.close()