# DeepNavigation

## Control Servo Motor Using Arduino

Here is a [good comparison](http://bioeng.nus.edu.sg/mm/wp-content/uploads/2012/07/MotorControl-1japwem.pdf) between servo motors and stepper motors.

- A servo motor includes a sensor, usually, a [potentiometer](https://en.wikipedia.org/wiki/Potentiometer), which is a three-terminal resistor with a sliding or rotating contact that forms an adjustable voltage divider.  This sensor helps the servo hold its position even if external force pushes against it.

- A stepper is a circle of electromagnets -- by activating a certain one, the shaft moves towards (and ideally very close to) the electromagnet.

Here is a good [introduction](https://www.digikey.com/en/articles/techzone/2017/mar/servo-motors-and-control-with-arduino-platforms)
to servo motors and Arduino controlling.

## Choose PVC Pipes

When people are talking about the diameter of PVC pipe, they mean the inner diameter (ID) instead of OD. [This article](https://www.pvcfittingsonline.com/resource-center/pvc-pipe-od-size-chart/) provides the mapping from the inner diameter (ID) to the outer diameter (OD) of PVC pipes: 

![](https://pvcfittingsonline.com/wordpress/wp-content/uploads/2016/04/PVC-Pipe-OD-Chart.jpg)

Deriving from data in the above table, we can compute the ratio of thickness over ID:

| ID   |  OD   | thickness | thickness / ID |
|------|-------|-----------|----------------|
| 0.5  | 0.84  | 0.34      | 0.68           |
| 0.75 | 1.05  | 0.3       | 0.4            |
| 1    | 1.315 | 0.315     | 0.315          |
| 1.25 | 1.66  | 0.41      | 0.328          |
| 1.5  | 1.9   | 0.4       | 0.266667       |
| 2    | 2.375 | 0.375     | 0.1875         |
| 3    | 3.5   | 0.5       | 0.166667       |

It seems that PVC pipes with ID=1.24 and 1.5 are the thickest (and supposedly strongest).

## Controlling DC Motors

Most servo motors can rotate for 180 degrees, so we’d prefer to control the DC motors for both clockwise and counterclockwise directions.

The control circuit for both directions is known as [H-bridge](http://www.modularcircuits.com/blog/articles/h-bridge-secrets/h-bridges-the-basics/), which works ad follows:

![](http://modularcircuits.com/blog/wp-content/uploads/2011/10/image7.png)

If Q1 and Q4 close but Q3 and Q2 open, the current flows through the DC motor from left to right.  If Q3 and Q2 close but Q1 and Q4 open, the current flows from right to left and the motor rotates in the opposite direction.

If both Q1 and Q2 close (or, Q3 and Q4 close), there would be a short circuit.

To prevent such illegal combinations, we can add two more transistors as the following:

![](images/h-bridge-no-shortcut.jpeg)

The above configuration cannot adjust the power of the DC. To do PWM of power, we can add an ENABLE signal, which is a 1.5V waveform. ICs like [L298](https://www.sparkfun.com/datasheets/Robotics/L298_H_Bridge.pdf) implements this method:

![](images/L298.jpeg)

## Battery

We have two Renogy RNG-BATT-GEL12-100 Deep Cycle [Pure Gel Batteries](https://www.amazon.com/gp/product/B01KN6QUW2/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1), each provide 12V and 100Ah capacity.

Lead-acid batteries should discard in no less than 5 hours, as fast discard might damad them. Suppose that we are going to discard a 60Ah battery in 5 hours, then the currency should be 100Ah / 5h = 20A.

Our [36 lbs DC motor](https://www.amazon.com/gp/product/B0713ZRFCC/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1) requires 29.5A current, as listed in the following table, so we need two batteries.

![](images/dc-motor-spec.png)



