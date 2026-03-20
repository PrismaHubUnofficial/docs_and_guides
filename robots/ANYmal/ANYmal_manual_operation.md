# ANYmal – Power, Charging, and Manual Operation Guide

<div style="text-align: center;">

![ANYmal Robot Image](./figures/anymal.jpg)

</div>

## Powering On ANYmal

To power on ANYmal, press the **black button**.  
Once pressed, the light on the robot will turn **white**, indicating that the boot sequence has started.

⚠️ **WARNING – Emergency Stop (E-STOP)**  
The **red emergency button (mushroom button)** immediately disconnects power from the actuators, causing the robot to collapse.  
If the emergency stop has been activated, **release it by rotating the button clockwise**, following the direction of the arrows printed on it.

---

## Charging ANYmal

To charge ANYmal:

1. Insert the **gray power cable** into the port located next to the power button.  
   Make sure the **red dots on the cable and on the port are aligned**.
2. Switch the charger lever to **ON**.

During charging, the charger LEDs **POWER**, **CONNECTED**, and **CHARGING** will be on.  
When charging is complete, **CHARGING** turns off and **FULL** turns on.

> ⚠️ It is possible for **FULL** and **CHARGING** to be on at the same time.  
> This corresponds to approximately **95% battery level**.

- **100% charge** ≈ **50.4 V**  
- **0% charge** (must never be reached) ≈ **40 V**

### Notes on Charging and Operation

- ANYmal **can be used while charging**, but special care must be taken not to damage the power cable.
- If ANYmal is powered on while charging and the **power cable is removed after the robot has received a “stand up” command**, the robot will assume it has undocked from a docking station and may take **a few autonomous steps**, even without joystick commands.

---

## Tablet and App Setup

After ANYmal is powered on:

1. Wait until the internal router has fully booted  
   (this is noticeable when the **fan noise increases**).
2. Turn on the **tablet**.
3. Ensure the tablet is connected to the Wi-Fi network  
   **`anymal-d138-wifi-2.4`**.
4. Open the **Field Operator App**  
   (Google Chrome icon on the home screen).

---

## Taking Control of the Robot

- In the **top-left corner** of the app, the status should show **“FREE”**.  
  Tap it and select **“Take Control”**.  
  The robot light will turn **yellow**, meaning it is ready to receive commands.

- If the **P-STOP** icon in the top-right corner has a **pink border**, tap it to disable the software stop.

- Under the **“OWNER”** label in the top-left corner, the mode must be **“MANUAL”**.  
  If it shows **“AUTO”**, tap it and select **“MANUAL”**.

---

## ANYmal Operation Modes

The main screen should display **five icons** representing the available modes.  
If they are not visible:

- Tap the **round icon in the bottom-right corner**
- Select the icon shaped like **ANYmal**

From **left to right**, the modes are:

1. **SLEEP Mode**  
   The robot sits down and **cuts power to the actuators**.

2. **SIT Mode**  
   The robot sits down, but the **actuators remain stiff**.

3. **TORSO CONTROL Mode**  
   The robot stands and interprets joystick commands as **angular positions**.

4. **WALK Mode**  
   The robot stands and interprets joystick commands as **linear velocities and yaw rate**.

5. **CHARGE Mode**  
   Not used, since no docking station is available.  
   The robot may incorrectly enter this mode if powered on while charging.

---

## Virtual Joystick

ANYmal uses a **virtual joystick**, accessible from the app:

- Tap the **round icon in the bottom-right corner**
- Select the **joystick-shaped icon**

---

## WALK Mode Controls

- **Single touch**
  - Vertical finger movement → forward/backward velocity along the robot’s heading
  - Horizontal finger movement → yaw velocity
  - Diagonal movement → circular trajectories

- **Double tap**
  - The robot translates while maintaining its orientation  
  - Enables **lateral walking** using horizontal finger movements

---

## TORSO CONTROL Mode Controls

- **Single touch**
  - Vertical finger movement → **pitch**
  - Horizontal finger movement → **yaw**

- **Double tap**
  - Enables **roll control**
  - Roll is adjusted using horizontal finger movements

---
