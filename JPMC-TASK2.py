From: Shubham Srivastava <shubhamsvt98@gmail.com>
Date:  Mon, 13 July 2020 
Subject: [PATCH] reate patch file

---
 node_modules.zip | Bin 0 -> 109310732 bytes
 src/App.tsx      |  27 +++++++++++++++++++++------
 src/Graph.tsx    |  15 ++++++++++++---
 3 files changed, 33 insertions(+), 9 deletions(-)
 create mode 100644 node_modules.zip

diff --git a/node_modules.zip b/node_modules.zip
new file mode 100644
index 0000000000000000000000000000000000000000..1a2295a48fe4694a62fe03a95ea205ba8f91e083
GIT binary patch
literal 109310732

literal 0
HcmV?d00001

diff --git a/src/App.tsx b/src/App.tsx
index 0728518..77c3fab 100755
--- a/src/App.tsx
+++ b/src/App.tsx
@@ -8,6 +8,7 @@ import './App.css';
  */
 interface IState {
   data: ServerRespond[],
+  showGraph: boolean,
 }
 
 /**
@@ -22,6 +23,7 @@ class App extends Component<{}, IState> {
       // data saves the server responds.
       // We use this state to parse data down to the child element (Graph) as element property
       data: [],
+      showGraph: false,
     };
   }
 
@@ -29,18 +31,31 @@ class App extends Component<{}, IState> {
    * Render Graph react component with state.data parse as property data
    */
   renderGraph() {
-    return (<Graph data={this.state.data}/>)
+    if(this.state.showGraph) {
+      return (<Graph data={this.state.data}/>)
+    }
   }
 
   /**
    * Get new data from server and update the state with the new data
    */
   getDataFromServer() {
-    DataStreamer.getData((serverResponds: ServerRespond[]) => {
-      // Update the state by creating a new array of data that consists of
-      // Previous data in the state and the new data from server
-      this.setState({ data: [...this.state.data, ...serverResponds] });
-    });
+    let x = 0;
+    const interval = setInterval(() => {
+      DataStreamer.getData((serverResponds: ServerRespond[]) => {
+        // Update the state by creating a new array of data that consists of
+        // Previous data in the state and the new data from server
+        this.setState ({
+          data: serverResponds ,
+          showGraph: true ,
+        });
+      });
+      x++;
+      if (x > 1000)
+      {
+        clearInterval(interval);
+      } 
+    }, 100);
   }
 
   /**
diff --git a/src/Graph.tsx b/src/Graph.tsx
index ec1430e..79094d5 100644
--- a/src/Graph.tsx
+++ b/src/Graph.tsx
@@ -1,5 +1,5 @@
 import React, { Component } from 'react';
-import { Table } from '@jpmorganchase/perspective';
+import { Table } from '@finos/perspective';
 import { ServerRespond } from './DataStreamer';
 import './Graph.css';
 
@@ -14,7 +14,7 @@ interface IProps {
  * Perspective library adds load to HTMLElement prototype.
  * This interface acts as a wrapper for Typescript compiler.
  */
-interface PerspectiveViewerElement {
+interface PerspectiveViewerElement extends HTMLElement{
   load: (table: Table) => void,
 }
 
@@ -32,7 +32,7 @@ class Graph extends Component<IProps, {}> {
 
   componentDidMount() {
     // Get element to attach the table from the DOM.
-    const elem: PerspectiveViewerElement = document.getElementsByTagName('perspective-viewer')[0] as unknown as PerspectiveViewerElement;
+    const elem = document.getElementsByTagName('perspective-viewer')[0] as unknown as PerspectiveViewerElement;
 
     const schema = {
       stock: 'string',
@@ -49,6 +49,15 @@ class Graph extends Component<IProps, {}> {
 
       // Add more Perspective configurations here.
       elem.load(this.table);
+      elem.setAttribute('view', 'y_line');
+      elem.setAttribute('column-pivots', '["stock"]');
+      elem.setAttribute('row-pivots', '["timestamp"]');
+      elem.setAttribute('columns','["top_ask_price"]');
+      elem.setAttribute('aggregates', `
+      {"stock": "discount count",
+      "top_ask_price":"avg",
+      "top_bid_price": "avg",
+      "timestamp":"distinct count"}`)
     }
   }
 
-- 
2.26.2 (Windows  Git-1)
