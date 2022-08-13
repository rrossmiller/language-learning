
// /***********************************************************************************************************************************/
// // Sets the global vars for the 3d transform. Any points sent through "process" will be transformed using these figures.
// // only needs to be called if Xan or Yan are changed.
// void SetVars(void)
// {
//   float Xan2, Yan2;
//   float s1, s2, c1, c2;

//   Xan2 = Xan / fact; // convert degrees to radians.
//   Yan2 = Yan / fact;

//   // Zan is assumed to be zero

//   s1 = sin(Yan2);
//   s2 = sin(Xan2);

//   c1 = cos(Yan2);
//   c2 = cos(Xan2);

//   xx = c1;
//   xy = 0;
//   xz = -s1;

//   yx = (s1 * s2);
//   yy = c2;
//   yz = (c1 * s2);

//   zx = (s1 * c2);
//   zy = -s2;
//   zz = (c1 * c2);
// }


// /***********************************************************************************************************************************/
// // processes x1,y1,z1 and returns rx1,ry1 transformed by the variables set in SetVars()
// // fairly heavy on floating point here.
// // uses a bunch of global vars. Could be rewritten with a struct but not worth the effort.
// void ProcessLine(struct Line2d *ret, struct Line3d vec)
// {
//   float zvt1;
//   int xv1, yv1, zv1;

//   float zvt2;
//   int xv2, yv2, zv2;

//   int rx1, ry1;
//   int rx2, ry2;

//   int x1;
//   int y1;
//   int z1;

//   int x2;
//   int y2;
//   int z2;

//   int Ok;

//   x1 = vec.p0.x;
//   y1 = vec.p0.y;
//   z1 = vec.p0.z;

//   x2 = vec.p1.x;
//   y2 = vec.p1.y;
//   z2 = vec.p1.z;

//   Ok = 0; // defaults to not OK

//   xv1 = (x1 * xx) + (y1 * xy) + (z1 * xz);
//   yv1 = (x1 * yx) + (y1 * yy) + (z1 * yz);
//   zv1 = (x1 * zx) + (y1 * zy) + (z1 * zz);

//   zvt1 = zv1 - Zoff;

//   if ( zvt1 < -5) {
//     rx1 = 256 * (xv1 / zvt1) + Xoff;
//     ry1 = 256 * (yv1 / zvt1) + Yoff;
//     Ok = 1; // ok we are alright for point 1.
//   }

//   xv2 = (x2 * xx) + (y2 * xy) + (z2 * xz);
//   yv2 = (x2 * yx) + (y2 * yy) + (z2 * yz);
//   zv2 = (x2 * zx) + (y2 * zy) + (z2 * zz);

//   zvt2 = zv2 - Zoff;

//   if ( zvt2 < -5) {
//     rx2 = 256 * (xv2 / zvt2) + Xoff;
//     ry2 = 256 * (yv2 / zvt2) + Yoff;
//   } else
//   {
//     Ok = 0;
//   }

//   if (Ok == 1) {

//     ret->p0.x = rx1;
//     ret->p0.y = ry1;

//     ret->p1.x = rx2;
//     ret->p1.y = ry2;
//   }
//   // The ifs here are checks for out of bounds. needs a bit more code here to "safe" lines that will be way out of whack, so they dont get drawn and cause screen garbage.

// }

// /***********************************************************************************************************************************/
// // line segments to draw a cube. basically p0 to p1. p1 to p2. p2 to p3 so on.
// void cube(void)
// {
//   // Front Face.

//   Lines[0].p0.x = -50;
//   Lines[0].p0.y = -50;
//   Lines[0].p0.z = 50;
//   Lines[0].p1.x = 50;
//   Lines[0].p1.y = -50;
//   Lines[0].p1.z = 50;

//   Lines[1].p0.x = 50;
//   Lines[1].p0.y = -50;
//   Lines[1].p0.z = 50;
//   Lines[1].p1.x = 50;
//   Lines[1].p1.y = 50;
//   Lines[1].p1.z = 50;

//   Lines[2].p0.x = 50;
//   Lines[2].p0.y = 50;
//   Lines[2].p0.z = 50;
//   Lines[2].p1.x = -50;
//   Lines[2].p1.y = 50;
//   Lines[2].p1.z = 50;

//   Lines[3].p0.x = -50;
//   Lines[3].p0.y = 50;
//   Lines[3].p0.z = 50;
//   Lines[3].p1.x = -50;
//   Lines[3].p1.y = -50;
//   Lines[3].p1.z = 50;


//   //back face.

//   Lines[4].p0.x = -50;
//   Lines[4].p0.y = -50;
//   Lines[4].p0.z = -50;
//   Lines[4].p1.x = 50;
//   Lines[4].p1.y = -50;
//   Lines[4].p1.z = -50;

//   Lines[5].p0.x = 50;
//   Lines[5].p0.y = -50;
//   Lines[5].p0.z = -50;
//   Lines[5].p1.x = 50;
//   Lines[5].p1.y = 50;
//   Lines[5].p1.z = -50;

//   Lines[6].p0.x = 50;
//   Lines[6].p0.y = 50;
//   Lines[6].p0.z = -50;
//   Lines[6].p1.x = -50;
//   Lines[6].p1.y = 50;
//   Lines[6].p1.z = -50;

//   Lines[7].p0.x = -50;
//   Lines[7].p0.y = 50;
//   Lines[7].p0.z = -50;
//   Lines[7].p1.x = -50;
//   Lines[7].p1.y = -50;
//   Lines[7].p1.z = -50;


//   // now the 4 edge lines.

//   Lines[8].p0.x = -50;
//   Lines[8].p0.y = -50;
//   Lines[8].p0.z = 50;
//   Lines[8].p1.x = -50;
//   Lines[8].p1.y = -50;
//   Lines[8].p1.z = -50;

//   Lines[9].p0.x = 50;
//   Lines[9].p0.y = -50;
//   Lines[9].p0.z = 50;
//   Lines[9].p1.x = 50;
//   Lines[9].p1.y = -50;
//   Lines[9].p1.z = -50;

//   Lines[10].p0.x = -50;
//   Lines[10].p0.y = 50;
//   Lines[10].p0.z = 50;
//   Lines[10].p1.x = -50;
//   Lines[10].p1.y = 50;
//   Lines[10].p1.z = -50;

//   Lines[11].p0.x = 50;
//   Lines[11].p0.y = 50;
//   Lines[11].p0.z = 50;
//   Lines[11].p1.x = 50;
//   Lines[11].p1.y = 50;
//   Lines[11].p1.z = -50;

//   LinestoRender = 12;
//   OldLinestoRender = LinestoRender;

// }
