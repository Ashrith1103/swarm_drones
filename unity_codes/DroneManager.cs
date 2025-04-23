using UnityEngine;
using System.Collections.Generic;

public class DroneManager : MonoBehaviour
{
    public GameObject dronePrefab;
    public GameObject packagePrefab;
    public Transform pickupPoint;
    public Transform[] dropOffPoints;

    private Queue<DroneAutopilot> droneQueue = new Queue<DroneAutopilot>();
    private int currentDropIndex = 0;

    void Start()
    {
        // Find all drones in the scene and set them up
        DroneAutopilot[] drones = FindObjectsOfType<DroneAutopilot>();
        
        if (drones.Length == 0)
        {
            Debug.LogError("No drones found in the scene!");
            return;
        }

        foreach (var drone in drones)
        {
            droneQueue.Enqueue(drone);
        }

        if (dropOffPoints.Length == 0)
        {
            Debug.LogError("No drop off points specified!");
            return;
        }

        StartNextDelivery();
    }

    void StartNextDelivery()
    {
        if (droneQueue.Count == 0)
        {
            Debug.Log("No drones available.");
            return;
        }

        DroneAutopilot drone = droneQueue.Dequeue();

        // Spawn the package at the pickup point
        GameObject package = Instantiate(packagePrefab, pickupPoint.position, Quaternion.identity);

        // Set drone parameters
        drone.pickupPoint = pickupPoint;
        drone.dropOffPoint = dropOffPoints[currentDropIndex];
        drone.package = package;

        // Register callback and start delivery
        drone.OnDeliveryComplete = () =>
        {
            // After delivery, move drone back to its initial position and reassign for next delivery
            droneQueue.Enqueue(drone); // Put drone back in queue after returning to start
            currentDropIndex = (currentDropIndex + 1) % dropOffPoints.Length; // Loop through drop-off points
            StartNextDelivery(); // Start next delivery
        };

        drone.StartDelivery(); // Start the current delivery
    }
}