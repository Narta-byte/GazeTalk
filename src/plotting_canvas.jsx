import React, { useState, useEffect } from 'react';
// import webgazer from 'webgazer';
import { docLoad, Restart } from './webgazer_utils';
import './PlottingCanvas.css';

const PlottingCanvas = () => {
  const [isDocLoaded, setIsDocLoaded] = useState(true);

  useEffect(() => {
    console.log("hello")
    const canvas = document.getElementById('plotting_canvas');
    if (isDocLoaded) {
      docLoad();
      setIsDocLoaded(false);
    }
    
      if (canvas) {
        // Restart(); // Initialize webgazer after the canvas is available
        webgazer
          .setRegression('ridge')
          .setTracker('TFFacemesh')
          .showVideoPreview(false)
          .setGazeListener((data, clock) => {
            if (data) {
              // console.log(data);
              const x = data.x
              const y = data.y
              const element = document.elementFromPoint(x,y)
              if (element.className === "tile") {
                console.log(element)

              }
            }
          })
          
          .begin();
      }
  }, []);

  return (
    <div>
      <div className="calibrationDiv">
        <input type="button" className="Calibration" id="Pt1" />
        <input type="button" className="Calibration" id="Pt2" />
        <input type="button" className="Calibration" id="Pt3" />
        <input type="button" className="Calibration" id="Pt4" />
        <input type="button" className="Calibration" id="Pt5" />
        <input type="button" className="Calibration" id="Pt6" />
        <input type="button" className="Calibration" id="Pt7" />
        <input type="button" className="Calibration" id="Pt8" />
        <input type="button" className="Calibration" id="Pt9" />
      </div>
      <canvas id="plotting_canvas" width="500" height="500"></canvas>
      {/* <li id="Accuracy">
        <a>Not yet Calibrated</a>
      </li> */}
    </div>
  );
};

export default PlottingCanvas;
