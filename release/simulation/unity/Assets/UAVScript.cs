using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;

using System.Net.Sockets;
using System.Threading;
using System.Timers;

public class UAVScript : MonoBehaviour
{
    private float counter;
    private float distance;

    private ArrayList listOfVectors = new ArrayList();


    //public Transform origin;
    //public Transform destination;

    public float lineDrawSpeed = 6f;


    public String host = "localhost";
    public Int32 port = 50004;

    float xCoor, yCoor, zCoor;


    internal Boolean socket_ready = false;
    internal String input_buffer = "";

    TcpClient tcp_socket;
    NetworkStream net_stream;

    StreamWriter socket_writer;
    StreamReader socket_reader;

    private void Start()
    {
        setupSocket();
    }

    void OnApplicationQuit()
    {
        closeSocket();
    }

    //setting up the communication
    public void setupSocket()
    {
        try
        {
            tcp_socket = new TcpClient(host, port);
            net_stream = tcp_socket.GetStream();
            socket_writer = new StreamWriter(net_stream);
            socket_reader = new StreamReader(net_stream);
            socket_ready = true;
            Debug.Log("established connection!");
        }
        catch (Exception e)
        {
            // Something went wrong
            Debug.Log("Socket error: " + e);
        }
    }

    //reading from a socket
    public String readSocket()
    {
        if (!socket_ready)
            return "";

        if (net_stream.DataAvailable)
        {
            Debug.Log("Something is being sent");
            return socket_reader.ReadLine();
        }

        return "";
    }

    //closing a socket
    public void closeSocket()
    {
        if (!socket_ready)
            return;

        socket_writer.Close();
        socket_reader.Close();
        tcp_socket.Close();
        socket_ready = false;
    }



    // Rigidbody - to get current positon, and set new position
    public Rigidbody rb;

    private void FixedUpdate()
    {
        string received_data = readSocket();
            Debug.Log("RECIEVED DATA :"  +received_data);
            String[] elements = received_data.Split(' ');

            foreach (var element in elements)
            {
                if (!String.IsNullOrEmpty(element))
                {
                    Debug.Log("Python controller sent: " + (string)element);
                    String[] strArr = element.Split(',');
                    xCoor = float.Parse(strArr[0]);
                    yCoor = float.Parse(strArr[1]);
                    zCoor = float.Parse(strArr[2]);
                }
                Simulate2(xCoor, yCoor, zCoor);

                // Simulate(element);
            }
            received_data = readSocket();

        Debug.Log("Nothing received");

    }


    void Simulate2(float x, float y, float z)
    {
        
        Vector3 newVector = new Vector3(x, y, z);
        Vector3 currentVector = rb.position;
        addLineVector(currentVector, newVector);
        rb.MovePosition(newVector);
    }

    void addLineVector(Vector3 currentVector, Vector3 newVector){
        // create a new line renderer
        LineRenderer lineRenderer = GetComponent<LineRenderer>();
        LineRenderer lRend = new GameObject().AddComponent<LineRenderer>();
        lRend.SetPosition(0, transform.position);
        lRend.SetWidth(.2f, .2f);
        lRend.SetPosition(1, newVector);
        listOfVectors.Add(lRend);
        lRend.SetColors(Color.blue, Color.blue);

        //lineRenderer.SetPosition(0, transform.position);
        //lineRenderer.SetWidth(.5f, .5f);
        //lineRenderer.SetPosition(1, newVector);
    }
}
