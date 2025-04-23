using UnityEngine;
using System;

public class DroneAutopilot : MonoBehaviour
{
    public Transform pickupPoint;
    public Transform dropOffPoint;
    public GameObject package;
    public float speed = 5f;
    public Action OnDeliveryComplete;

    private bool isActive = false;
    private bool packagePickedUp = false;
    private bool returningToStart = false;

    private Vector3 startPosition;

    void Start()
    {
        startPosition = transform.position;
    }

    void Update()
    {
        if (!isActive && !returningToStart) return;

        if (returningToStart)
        {
            MoveTo(startPosition);

            if (Vector3.Distance(transform.position, startPosition) < 0.2f)
            {
                returningToStart = false;
                Debug.Log($"{gameObject.name} returned to start.");
                OnDeliveryComplete?.Invoke(); // Notify manager to assign next delivery
            }

            return;
        }

        if (!packagePickedUp)
        {
            MoveTo(pickupPoint.position);

            if (Vector3.Distance(transform.position, pickupPoint.position) < 0.2f)
            {
                package.transform.SetParent(transform);
                package.transform.localPosition = new Vector3(0, -0.5f, 0);
                packagePickedUp = true;
                Debug.Log($"{gameObject.name} picked up the package");
            }
        }
        else
        {
            MoveTo(dropOffPoint.position);

            if (Vector3.Distance(transform.position, dropOffPoint.position) < 0.2f)
            {
                package.transform.SetParent(null);
                package.transform.position = dropOffPoint.position;

                isActive = false;
                packagePickedUp = false;
                returningToStart = true;

                Debug.Log($"{gameObject.name} dropped off the package, returning to start...");
            }
        }
    }

    public void StartDelivery()
    {
        isActive = true;
        returningToStart = false;
    }

    private void MoveTo(Vector3 target)
    {
        Vector3 dir = target - transform.position;
        transform.Translate(dir.normalized * speed * Time.deltaTime, Space.World);
    }
}
