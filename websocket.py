import UIKit
import CoreMotion
import Foundation

class ViewController: UIViewController {
    let motionManager = CMMotionManager()
    var webSocketTask: URLSessionWebSocketTask?

    override func viewDidLoad() {
        super.viewDidLoad()

        if motionManager.isMagnetometerAvailable {
            motionManager.magnetometerUpdateInterval = 0.1
            motionManager.startMagnetometerUpdates(to: OperationQueue.main) { [weak self] (data, error) in
                if let validData = data {
                    let x = validData.magneticField.x
                    let y = validData.magneticField.y
                    let heading = atan2(y, x) * 180 / .pi
                    self?.sendCompassData(heading: heading)
                }
            }
        } else {
            print("Magnetometer is not available on this device.")
        }

        connectToWebSocket()
    }

    func connectToWebSocket() {
        let url = URL(string: "ws://localhost:8765")!
        webSocketTask = URLSession(configuration: .default).webSocketTask(with: url)
        webSocketTask?.resume()
    }

    func sendCompassData(heading: Double) {
        let message = URLSessionWebSocketTask.Message.string("Heading: \(heading)")
        webSocketTask?.send(message) { error in
            if let error = error {
                print("WebSocket sending error: \(error)")
            }
        }
    }

    deinit {
        webSocketTask?.cancel(with: .goingAway, reason: nil)
    }
}